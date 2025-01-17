import json
import logging
from model.parsed import ParsedAudit
import traceback
from datetime import timedelta
from typing import Any, Dict, List, Tuple
from uuid import UUID, uuid4
from pydantic.types import Json, UUID4
from starlette.responses import JSONResponse

from pytz import timezone
from datetime import datetime, timedelta

from core.config import settings
from crud import audits as crud_audit
from crud import category as crud_category
from crud import parsed as crud_parsed
from crud import parsed_questions as crud_pq
from crud import premises as crud_premise
from crud import question as crud_questions
from model import User
from schema import SubmitSchema, ParsedAuditCreate
from pony.orm.core import flush
from pony.orm import Json

from .clean import strip_markdown
from .s3_helper import store_raw_data, delete_raw_data

UK_DATE_FORMAT = "%d %B %Y at %H:%M"

logger = logging.getLogger(__name__)


def make_image_url(iid):
    # Make sure this is only used inside a flask context or things break
    return settings.IMAGE_URl + "/audit/photo/" + iid


def format_duration(duration: timedelta):
    seconds = duration.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    hours = int(hours)
    minutes = int(minutes)

    return f'{hours} hour{"s" if hours != 1 else ""}, {minutes} minute{"s" if minutes != 1 else ""}'


def get_summed_failures_across_one_site(
    premises: UUID, template: UUID
) -> Tuple[List[str], List[int], List[int]]:
    titles = []
    numbers = []
    failures = []

    at = crud_audit.get_by_uuid(uuid=template)

    question_order = {str(q.question.uuid): q.order for q in at.questions}

    full_cats = [c.category for c in at.categories]

    challenge_questions = [
        q.uuid for c in full_cats for q in c.questions if c.challenge
    ]

    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=premises, template=template
    )

    pqs = crud_pq.get_failed_question_and_count(
        reports=reports,
        challenge_questions=challenge_questions,
        sort_by={"desc": True, "sort_by": 2},
        limit=9,
    )
    for uuid, fc in pqs:
        q = crud_pq.get_by_uuid(uuid=uuid)

        if str(q.question.uuid) not in [q.question.uuid for q in at.questions]:
            continue

        stripped = strip_markdown(q.question.text)
        titles.append(stripped if len(stripped) < 240 else stripped[:240] + "...")
        numbers.append(int(question_order[str(q.question.uuid)]) + 1)  # 0 indexed
        failures.append(fc)

    return titles, numbers, failures


def get_summed_failures_across_all_sites(
    premises: UUID, template: UUID
) -> Tuple[List[str], List[int], List[int]]:
    titles = []
    numbers = []
    failures = []

    original = crud_premise.get_by_uuid(uuid=premises)
    group_list = crud_premise.get_group_list(obj_in=original)

    at = crud_audit.get_by_uuid(uuid=template)

    question_order = {str(q.question.uuid): q.order for q in at.questions}

    full_cats = [c.category for c in at.categories]

    challenge_questions = [
        q.uuid for c in full_cats for q in c.questions if c and c.challenge
    ]

    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=group_list, template=template, group=True
    )

    pqs = crud_pq.get_failed_question_and_count(
        reports=reports,
        challenge_questions=challenge_questions,
        sort_by={"desc": True, "sort_by": 2},
        limit=9,
    )

    for uuid, fc in pqs:

        q = crud_pq.get_by_uuid(uuid=uuid)

        if str(q.question.uuid) not in [str(q.question.uuid) for q in at.questions]:
            continue

        stripped = strip_markdown(q.question.text)
        titles.append(stripped if len(stripped) < 240 else stripped[:240] + "...")
        numbers.append(int(question_order[str(q.question.uuid)]) + 1)  # 0 indexed
        failures.append(fc)

    return titles, numbers, failures


def get_rolling_scores_for_one_site(premises: UUID, template: UUID):
    dates = []
    scores = []

    sort_by = {"desc": True, "sort_by": "a.end_time"}
    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=premises, template=template, limit=12, sort_by=sort_by
    )

    for r in reports:
        dates.append(
            r.end_time.strftime("%d-%m-%Y")
            if settings.UK_DATE
            else r.end_time.strftime("%m-%d-%Y")
        )
        scores.append(r.score_percentage * 100)

    return dates, scores


def get_rolling_scores_for_all_sites(premises: UUID, template: UUID):
    result = []

    original = crud_premise.get_by_uuid(uuid=premises)
    group_list = group_list = crud_premise.get_group_list(
        obj_in=original, premises=True
    )

    sites_uuids = [p.uuid for p in group_list]
    site_names = {str(p.uuid): p.name for p in group_list}

    sort_by = {"desc": True, "sort_by": "a.end_time"}
    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=sites_uuids, template=template, group=True, limit=12, sort_by=sort_by
    )

    for guuid in sites_uuids:
        dates = []
        scores = []

        for r in reports:
            if r.premises == guuid:
                dates.append(
                    r.end_time.strftime("%d-%m-%Y")
                    if settings.UK_DATE
                    else r.end_time.strftime("%m-%d-%Y")
                )
                scores.append(r.score_percentage * 100)

        if dates and scores:
            result.append((site_names[str(guuid)], dates[:4], scores[:4]))

    return result


def get_failures_by_section_for_one_site(premises: UUID, template: UUID):
    section_names = []
    failures = []
    uuids = []

    at = crud_audit.get_by_uuid(uuid=template)

    cat_order = {c.category.uuid: c.order for c in at.categories}

    category_uuids = [str(c.category.uuid) for c in at.categories]

    full_cats = [c.category for c in at.categories]

    challenge_questions = [
        q.uuid for c in full_cats for q in c.questions if c.challenge
    ]

    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=premises, template=template
    )

    sort_by = {"desc": True, "sort_by": 2}

    pcs = crud_pq.get_failed_category_and_count(
        challenge_questions=challenge_questions,
        reports=reports,
        limit=7,
        sort_by=sort_by,
    )

    for uuid, fc in pcs:
        if str(uuid) not in category_uuids:
            continue

        c = crud_category.get_by_uuid(uuid=uuid)

        if c.challenge:
            continue

        if c.parent is not None:
            cp = crud_category.get_by_uuid(uuid=c.parent)
            if cp.text in section_names:
                failures[section_names.index(cp.text)] += fc
            else:
                section_names.append(cp.text)
                failures.append(fc)
        else:
            if c.text in section_names:
                failures[section_names.index(c.text)] += fc
            else:
                section_names.append(c.text)
                failures.append(fc)
                uuids.append(str(c.uuid))

    if len(failures) > 0:
        bundle = list(zip(section_names, failures, uuids))
        bundle.sort(key=lambda x: cat_order[x[2]])

        section_names, failures, _ = list(zip(*bundle))

    return section_names, failures


def get_failures_by_section_for_all_sites(premises: UUID, template: UUID):
    section_names = []
    failures = []

    original = crud_premise.get_by_uuid(uuid=premises)

    group_list = group_list = crud_premise.get_group_list(obj_in=original)

    at = crud_audit.get_by_uuid(uuid=template)

    category_uuids = [str(c.category.uuid) for c in at.categories]

    full_cats = [c.category for c in at.categories]

    challenge_questions = [
        q.uuid for c in full_cats for q in c.questions if c.challenge
    ]

    reports = crud_parsed.get_parsed_audits_by_template_and_premises(
        premises=group_list, template=template, group=True
    )
    sort_by = {"desc": True, "sort_by": 2}

    pcs = crud_pq.get_failed_category_and_count(
        challenge_questions=challenge_questions,
        reports=reports,
        limit=7,
        sort_by=sort_by,
    )

    for uuid, fc in pcs:
        if str(uuid) not in category_uuids:
            continue

        c = crud_category.get_by_uuid(uuid=uuid)

        if c.challenge:
            continue

        if c.parent is not None:
            cp = crud_category.get_by_uuid(uuid=c.parent)

            if cp.text in section_names:
                failures[section_names.index(cp.text)] += fc
            else:
                section_names.append(cp.text)
                failures.append(fc)
        else:
            if c.text in section_names:
                failures[section_names.index(c.text)] += fc
            else:
                section_names.append(c.text)
                failures.append(fc)

    return section_names, failures


def update_images(
    obj_in: SubmitSchema, scored_audit: UUID4, user: UUID4, location: UUID4
):
    """Update Images with parsed audit uuid

    Args:
        scored_audit (UUID4): The parsed audit uuid
        user (UUID4): The auditor uuid
        location (UUID4): The loactaion uuid
    """

    questions_list_sep = list(
        map(
            lambda category: [questions for questions in category["questions"]],
            [category for category in obj_in.body],
        )
    )

    questions_with_photo  = []

    for questions in questions_list_sep:
        for question in questions:
            has_photo = question.get("photo_url", "")
            if has_photo:
                questions_with_photo.append(question)

    for q in questions_with_photo:

        urls = q["photo_url"]
        # Split the URL string at each "/" character and extract the last element

        if isinstance(urls, list):
            d_imgs = [crud_audit.get_image_by_uuid(uuid=UUID((url.split("/")[-1]).split(".")[0])) for url in urls]

        d_imgs = [crud_audit.get_image_by_uuid(uuid=UUID((urls.split("/")[-1]).split(".")[0]))]
        
        if d_imgs:
            for d_img in d_imgs:
                parsed_question = crud_pq.get_by_question_and_audit(question=str(q.get("uuid", "")), audit=str(scored_audit.uuid))

                if parsed_question is None:
                    parsed_question = crud_pq.get_by_uuid(uuid=str(q.get("uuid", "")))

                if parsed_question is not None:
                    crud_audit.update_audit_image(
                        db_obj=d_img, obj_in={"parsed_audit": scored_audit, "parsed_question": parsed_question}
                    )


def save_parsed_audit(obj_in: SubmitSchema, user: User):
    """Saved Parsed Audit for User

    Args:
        obj_in (SubmitSchema): The Submit Schema
        user (User): The User model object

    Returns:
        Dict[str, Any]: The return dictionary
    """
    l_uuid = UUID(obj_in.location)

    location = crud_premise.get_by_uuid(uuid=l_uuid)

    if not location:
        return {
            "success": False,
            "status_code": 422,
            "message": "No such location or resource by that UUID or name",
        }

    parsed_audit_uuid = uuid4()

    res = store_raw_data(location=location.name, _object=obj_in.json(), uuid=str(parsed_audit_uuid))
    if not res["success"]:
        return {"success": False, "status_code": 403, "message": "Access Denied on Aws"}
    uri, key = res["uri"], res["obj_key"]

    scored_audit = ParsedAuditCreate(
        uuid=parsed_audit_uuid,
        audit_template=obj_in.type,
        premises=obj_in.location,
        user=user.uuid,
        final_comments=obj_in.comments,
        timezone=obj_in.timezone,
        extra=obj_in.extra,
        start_time=obj_in.stime.replace(tzinfo=None),  # TODO: Test tz issue more
        end_time=obj_in.etime.replace(tzinfo=None),
        raw_data_key=key,
        raw_data_uri=uri,
    )

    persisted_audit = crud_parsed.create(obj_in=scored_audit.dict(exclude_unset=True))
    
    flush()

    get_audit_summary_and_cat_order(obj_in.body, persisted_audit)
    # Finish parsing
    
    return {
        "success": True, 
        "result": {
            "location": location,
            "scored_audit": crud_parsed.get_by_uuid(uuid=persisted_audit.uuid)
            }
        }


def get_audit_summary_stats(body: Json):
    audit_summary_stats = []

    for category in body:
        skipped = [q for q in category["questions"] if "skipped" in q]
        passed = [q for q in category["questions"] if "pass" in q and q["pass"]]
        total_failed = len(category["questions"]) - len(passed) - len(skipped)
        built_summary_stats = [
            category["text"],
            len(category["questions"]) - len(skipped),
            len(passed),
            total_failed,
        ]
        audit_summary_stats.append(built_summary_stats)

    return audit_summary_stats


def get_audit_summary_and_cat_order(body: Json, scored_audit: ParsedAudit, is_new: bool = True):
    # category_order = []
    actual_score, possible_score = 0, 0

    for category in body:
        passed = [q for q in category["questions"] if "pass" in q and q["pass"]]

        max_score = sum(q["worth"] for q in category["questions"] if "skipped" not in q)
        cat_score = sum(q["worth"] for q in passed)

        actual_score += cat_score
        possible_score += max_score

        # category_order.append(UUID(category['uuid']))

        for q in category["questions"]:
            if "skipped" in q:
                # Is this the best way to handle this? No clue
                continue
            temp_dict = {
                "category": crud_category.get_by_uuid(uuid=category["uuid"]),
                "parsed_audit": scored_audit,
                "worth": q["worth"],
                "passed": "pass" in q and q["pass"]
            }

            temp_dict["notes"] = q.get("notes", q.get("note", ""))

            saved_pq = None

            if not is_new:
                saved_pq = crud_pq.get_by_question_and_audit(question=str(q["uuid"]), audit=str(scored_audit.uuid))

                if saved_pq is None:
                    saved_pq = crud_pq.get_by_uuid(uuid=str(q["uuid"]))

            saved_question = None

            if saved_pq is not None:
                saved_question = saved_pq.question

            if saved_question is None:
                temp_dict["question"] = crud_questions.get_by_uuid(uuid=q["uuid"])

            else:
                temp_dict["question"] = saved_question

            if is_new:
                d_pq = crud_pq.create(obj_in=temp_dict)
            else:
                d_pq = crud_pq.get_by_question_and_audit(question=str(q["uuid"]), audit=str(scored_audit.uuid))

                if d_pq is None:
                    d_pq = crud_pq.get_by_uuid(uuid=str(q["uuid"]))
                                               
                if d_pq is not None:
                    d_pq.set(**temp_dict)

            flush()

    scored_percentage = 0

    if possible_score > 0:
        scored_percentage = round(actual_score / possible_score, 2)


    crud_parsed.update(
        db_obj=scored_audit, 
        obj_in={
            "score": actual_score,
            "max_score": possible_score,
            "score_percentage": scored_percentage,
    })

    return actual_score, possible_score


def remap(
    scored_audit: ParsedAuditCreate, user: User, obj_in: SubmitSchema
) -> Dict[str, Any]:

    l_uuid = scored_audit.premises

    location = crud_premise.get_by_uuid(uuid=l_uuid)
    group = crud_premise.get_premsise_group_by_uuid(uuid=location.group)
    manager_dets = crud_premise.get_manager_details(uuid=location.uuid)
    audit_summary_stats = get_audit_summary_stats(obj_in.body)
    # audit_object = crud_premise.get_by_uuid(uuid=l_uuid)
    template = crud_audit.get_by_uuid(uuid=scored_audit.audit_template.uuid)

    _type = scored_audit.audit_template.uuid

    audit_delta: timedelta = scored_audit.end_time - scored_audit.start_time
    
    tz = timezone(scored_audit.timezone if scored_audit.timezone else settings.API_TIMEZONE)
    now = datetime.now(tz)
    offset = now.utcoffset()
    offset_hours = offset.days * 24 + offset.seconds // 3600
    
    bst_start = scored_audit.start_time + timedelta(hours=offset_hours)
    bst_end = scored_audit.end_time + timedelta(hours=offset_hours)
    
    remap_metadata = [
        ("Start Time", bst_start.strftime(UK_DATE_FORMAT), "far fa-clock"),
        ("End Time", bst_end.strftime(UK_DATE_FORMAT), "far fa-clock"),
        ("Audit Duration", format_duration(audit_delta), "fas fa-hourglass-half"),
        ("Auditor", user.name, "far fa-user"),
        ("Site", location.name, "fas fa-map-marker-alt"),
        (
            "Site Group",
            group.name if group else "N/A (No Group)",
            "fas fa-globe-americas",
        ),
        ("Site Manager", manager_dets.name if manager_dets is not None else "None", "fas fa-user-tie"),
        (
            "Score",
            f"{(scored_audit.score_percentage * 100):.0f}%",
            "fas fa-flag-checkered",
        ),
        (
            "Location Average Score",
            f"{(scored_audit.score_percentage * 100):.0f}%",
            "fas fa-flag-checkered",
        ),
        (
            "Final Comments",
            scored_audit.final_comments,
            "fas fa-flag-checkered",
        ),
        (
            "Template",
            template.name,
            "fas fa-flag-checkered",
        ),
    ]

    # sort_by = {"desc": True, "sort_by": "a.end_time"}
    # last_audit = crud_parsed.get_audit(uuid=location.uuid, sort_by=sort_by, first=True)
    #
    # if last_audit:
    #     bst_last_end = last_audit.end_time.astimezone(bst)
    #     remap_metadata.append(
    #         (
    #             "Location Average Score",
    #             bst_last_end.strftime(UK_DATE_FORMAT),
    #             "fas fa-history",
    #         )
    #     )
    # else:
    #     remap_metadata.append(
    #         ("Location Average Score", "No previous audits", "fas fa-history")
    #     )

    # object passed into the PDF generator
    final_remap = {
        "report_metadata": remap_metadata,
        "audit_summary_stats": audit_summary_stats,
    }

    if scored_audit.final_comments:
        # TODO: duplicate data
        final_remap["final_comments"] = scored_audit.final_comments

    if scored_audit.extra:
        final_remap["extra"] = scored_audit.extra

    if obj_in.signatory:
        final_remap["signature_info"] = obj_in.signatory

    # Summed failures for this site
    try:
        (
            qt_on_this_site,
            qn_on_this_site,
            fc_on_this_site,
        ) = get_summed_failures_across_one_site(location.uuid, _type)

        final_remap["summed_failures_for_this_site"] = {
            "titles": qt_on_this_site,
            "questions": qn_on_this_site,
            "failures": fc_on_this_site,
        }
    except Exception as e:
        logger.error("Error in Summed failures for this site")
        logger.error(traceback.format_exc())

    try:
        (
            qt_on_all_sites,
            qn_on_all_sites,
            fc_on_all_sites,
        ) = get_summed_failures_across_all_sites(location.uuid, _type)

        final_remap["summed_failures_for_all_sites"] = {
            "titles": qt_on_all_sites,
            "questions": qn_on_all_sites,
            "failures": fc_on_all_sites,
        }
    except Exception as e:
        logger.error("Error in Summed failures for all sites")
        logger.error(traceback.format_exc())

    # Rolling scores for one site
    try:
        dates_for_this_site, scores_for_this_site = get_rolling_scores_for_one_site(
            location.uuid, _type
        )

        final_remap["rolling_scores_for_this_site"] = {
            "dates": dates_for_this_site,
            "scores": scores_for_this_site,
        }
    except Exception as e:
        logger.error("Error in Rolling scores for one site")
        logger.error(traceback.format_exc())

    # Rolling scores for all sites (in group)
    try:
        scores_for_all_sites = get_rolling_scores_for_all_sites(location.uuid, _type)

        logger.error(f"Got {len(scores_for_all_sites)} sites")

        final_remap["rolling_scores_for_all_sites"] = {
            site_name: {"dates": dates, "scores": scores}
            for site_name, dates, scores in scores_for_all_sites
        }
    except Exception as e:
        logger.error("Error in Rolling scores for all sites")
        logger.error(traceback.format_exc())

    # Failures by category for one site
    try:
        (
            sections_for_this_site,
            failures_for_this_site,
        ) = get_failures_by_section_for_one_site(location.uuid, _type)

        final_remap["failures_by_section_for_this_site"] = {
            "sections": sections_for_this_site,
            "failures": failures_for_this_site,
        }
    except Exception as e:
        logger.error("Error in Failures by category for one site")
        logger.error(traceback.format_exc())

    # Failures by category for all sites (in group)
    try:
        (
            sections_for_all_sites,
            failures_for_all_sites,
        ) = get_failures_by_section_for_all_sites(location.uuid, _type)

        final_remap["failures_by_section_for_all_sites"] = {
            "sections": sections_for_all_sites,
            "failures": failures_for_all_sites,
        }
    except Exception as e:
        logger.error("Error in Failures by category for all sites")
        logger.error(traceback.format_exc())

    sf_data = []
    header_colors = {}

    for category in obj_in.body:
        if "challenge" in category:
            challenges = []

            for q in category["questions"]:
                if "notes" in q and "pass" in q:
                    challenges.append(
                        (
                            int(q["order"]) + 1,
                            q["text"],
                            q["hint"]["text"],
                            q.get("notes", q.get("note", "")),
                            "Pass" if q["pass"] else "Fail",
                        )
                    )

                if len(challenges) >= 5:
                    break

            final_remap["competence_questions"] = challenges
            continue

        q_data = []

        for q in category["questions"]:
            _include_pass = settings.INCLUDE_PASS
            _include_na = settings.INCLUDE_NA
            _include_no = settings.INCLUDE_NO
            _has_pass = "pass" in q
            _has_na = "skipped" in q
            _has_no = "unknown" in q

            _pass_check = _has_pass and (not q["pass"] if not _include_pass else True)
            _na_check = _has_na and not _has_pass if _include_na else False
            _no_check = _has_no and not _has_pass if _include_no else False

            if _pass_check or _na_check or _no_check:      

                parsed_images = q.get("images", q.get("photo_url", ""))   

                if not parsed_images:
                    photos = q.get("photos", "")

                    if photos and isinstance(photos, list):
                       parsed_images = []
                       for photo in photos:
                           if not photo["markedForDeletion"] and  photo["serverUUID"]:
                                img = crud_audit.get_image_by_uuid(uuid=UUID(photo["serverUUID"]))
                                if img:
                                    parsed_images.append(img.image_uri)
                                    parsed_question = crud_pq.get_by_question_and_audit(question=photo.get("questionUUID", ""), audit=str(scored_audit.uuid))
                                    if parsed_question:
                                        img.parsed_question = parsed_question
                                    parsed_audit = crud_parsed.get_by_uuid(uuid=str(scored_audit.uuid))
                                    if parsed_audit:
                                        img.parsed_audit = parsed_audit

                if isinstance(parsed_images, str):
                    parsed_images = [parsed_images]     

                iq_data = {
                    "question_number": q["order"] + 1,
                    "question_title": strip_markdown(q["text"]),
                    "question_description": strip_markdown(q["text"]),
                    "nonconformance": q.get("notes", q.get("note", "")),
                    "images": parsed_images,
                }

                if "pass" in q:
                    iq_data["pass"] = q["pass"]

                if "unknown" in q:
                    iq_data["unknown"] = q["unknown"]

                if "reference" in q:
                    iq_data["reference"] = q["reference"]
                    
                if iq_data.get("nonconformance") or parsed_images != [''] or iq_data.get("pass") is False:
                    q_data.append(iq_data)

        q_data.sort(key=lambda q: q["question_number"])

        sf_data.append([category["text"], q_data])

        dc = crud_category.get_by_uuid(uuid=UUID(category["uuid"]))

        header_colors[category["text"]] = dc.color

    final_remap["header_colors"] = header_colors
    final_remap["failures_for_this_audit"] = sf_data

    # TODO: refactor
    def _generate_pagedata(records):
        rowsCnt = 5
        result = []
        rowsPerPage = []
        for index, record in enumerate(records):
            if not "pass" in record:
                record["pass"] = "NA"
            if len(record["images"]) == 0:
                rowsCnt = rowsCnt - 1
            else:
                rowsCnt = rowsCnt - round(len(record["images"]) / 2) * 2
            rowsPerPage.append(record)
            if (rowsCnt <= 0) or index == len(records) - 1:
                rowsCnt = 5
                result.append(rowsPerPage)
                rowsPerPage = []
        return result

    _new_data = []
    for section_name, questions in final_remap["failures_for_this_audit"]:
        _new_data.append((section_name, _generate_pagedata(questions)))
    final_remap["failures_for_this_audit"] = _new_data

    image_urls = []

    for attribute in _new_data:
        for question_list in attribute[1]:
            for question in question_list:
                if 'images' in question and question['images'] != ['']: # Only include if images list is not empty
                    for image_url in question['images']:
                        image_urls.append({
                            'question_number': question['question_number'],
                            'question_title': question['question_title'],
                            'comment_title': question['nonconformance'],
                            'image_url': image_url
                        })


    final_remap["failures_audit_images"] = image_urls

    # END TODO

    if settings.BADGE:
        final_remap["badge"] = True
    # End remapping

    stupid_object = json.dumps(final_remap)

    logger.info("This is going to be print on the pdf", stupid_object)

    return {
        "final_remap": stupid_object,
        "location": location,
        "scored_audit": scored_audit,
    }


def update_parsed_audit(obj_in: SubmitSchema, user: User, parsed_audit: ParsedAudit):

    """Update Parsed Audit for User

    Args:
        obj_in (SubmitSchema): The Submit Schema
        user (User): The User model object

    Returns:
        Dict[str, Any]: The return dictionary
    """
    l_uuid = UUID(obj_in.location)

    if not obj_in.location:
        l_uuid = parsed_audit.premises

    location = crud_premise.get_by_uuid(uuid=l_uuid)

    if not location:
        return {
            "success": False,
            "status_code": 422,
            "message": "No such resource by that UUID or name",
        }
    json_result = json.dumps(parsed_audit.build_json_result())

    raw_data_key = parsed_audit.raw_data_key
    
    delete_exising_audit = delete_raw_data(full_name=raw_data_key)

    if not delete_exising_audit["success"]:
        return JSONResponse(
            status_code=400,
            content={"message": "Error deleting resource"},
        )

    res = store_raw_data(location=location.name, _object=json_result, uuid=str(parsed_audit.uuid))
    if not res["success"]:
        return {"success": False, "status_code": 403, "message": "Access Denied on Aws"}
    uri, key = res["uri"], res["obj_key"]
    obj_dict = obj_in.dict(exclude_none=True, exclude_unset=True)

    obj_dict.pop("body", None)
    obj_dict.pop("location", None)
    obj_dict.pop("type", None)
    obj_dict.pop("etime", None)
    obj_dict.pop("stime", None)

    update_obj = {
        "user": user.uuid,
        "raw_data_key": key,
        "raw_data_uri": uri,
        "premises": l_uuid,
        **obj_dict,
    }
    parsed_audit.set(**update_obj)

    flush()

    get_audit_summary_and_cat_order(
        obj_in.body, parsed_audit, False
    )
    # Finish parsing

    result = {
        "location": location,
        "scored_audit": crud_parsed.get_by_uuid(uuid=str(parsed_audit.uuid)),
    }

    return {"success": True, "result": result}

def update_images_by_editor(obj_in: SubmitSchema, scored_audit: UUID4, user: UUID4, location: UUID4):
    questions_list_sep = list(
        map(
            lambda category: [questions for questions in category["questions"]],
            [category for category in obj_in.body],
        )
    )

    questions_with_photo  = []

    for questions in questions_list_sep:
        for question in questions:
            has_photo = question.get("photo_url", "")
            if has_photo:
                questions_with_photo.append(question)

    for q in questions:

        d_imgs = crud_pq.get_by_uuid(uuid=str(q.get("uuid", ""))).images if crud_pq.get_by_uuid(uuid=str(q.get("uuid", ""))) else []

        for d_img in d_imgs:
                parsed_question = crud_pq.get_by_uuid(uuid=str(q.get("uuid", "")))

                if parsed_question is not None:
                    crud_audit.update_audit_image(
                        db_obj=d_img, obj_in={"parsed_audit": scored_audit, "parsed_question": parsed_question}
                    )