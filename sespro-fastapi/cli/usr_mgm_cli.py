import json
from typing import Any, Callable, Dict, Optional, Union
import uuid
from click.utils import echo
from pony.orm.core import flush
from pydantic.types import UUID4

import typer

from model.user import User
from pony.orm import db_session, commit
from pydantic import ValidationError

from crud import user as crud_user, manager as crud_manager, premises as crud_premises
from schema import EmailSchema, Register, RegisterOut
from database import create_all_tables

MAIN_MENU: Dict[int, str] = {
    1: "Create A New User",
    2: "Edit An Existing User",
    0: "Exit Process"
}

PREMISES: Dict[int, str] = {
    1: "Edit",
    2: "Add New Premises",
    3: "Remove Premises",
    0: "Exit Process"
}

AFTER_USER_CREATION: Dict[int, str] = {
    1: "Edit User Details",
    2: "Add User to Premise",
    3: "Create Another User",
    0: "Done"
}

ADD_PREMISE: Dict[int, str] = {
    1: "Create New",
    2: "Add Existing",
    3: "Go Back",
    0: "Exit Process"
}


def check_options(_input: int,
                  obj: Dict[int, Any],
                  level: int,
                  data: Optional[Dict[str, Any]] = None):
    """Check the option selected available 

    Raises:
        typer.Exit: The cli scripts exits

    Returns:
        Callable : calls the engine function
    """

    if _input not in obj:
        typer.secho("Wrong Input", fg=typer.colors.RED)
        return show_options(reload=True)

    if _input == 0:
        typer.secho("Aborted!", fg=typer.colors.RED)
        raise typer.Exit(code=0)

    if data:
        return engine(num=_input, level=level, data=data)

    return engine(num=_input, level=level)


def show_options(data: Optional[Dict[str, Any]] = None,
                 reload: bool = False,
                 obj: Optional[Dict[int, Any]] = MAIN_MENU,
                 level: int = 1) -> int:
    """Show the options in the dict

    Args:
        data (Optional[Dict[str, Any]], optional): the data from the previous call. Defaults to None.
        reload (bool, optional): should reload on werong input. Defaults to False.
        obj (Optional[Dict[int, Any]], optional): The options to show. Defaults to MAIN_MENU.
        level (int, optional): The level in the engine. Defaults to 1.

    Returns:
        Callable: calls the check_option
    """
    typer.echo("")
    if reload:
        typer.secho("Lets do that again!",
                    fg=typer.colors.BLACK,
                    bg=typer.colors.WHITE)

    for i in obj.keys():
        typer.secho(f'{i} - {obj[i]}')

    answer = typer.prompt(text="What number would it be for you?",
                          default=0,
                          type=int)
    if data:
        return check_options(answer, obj=obj, level=level, data=data)
    return check_options(answer, obj=obj, level=level)


def create_user(user: Register) -> User:
    user_dict: Dict[str, Any] = user.dict()
    password = user_dict["password"]
    user_dict["active"] = True
    user = User(**user_dict)
    user.set_password(password=password)
    commit()
    """try:
        commit()
    except Exception:
        return False"""

    return user


def get_user_detail(email: str) -> User:
    """Get user details

    Args:
        email (str): the user email

    Returns:
        User: The User Object
    """
    user = crud_user.get_by_email(email=email)
    return user


def update_user(data: Dict[str, Any],
                db_obj: User,
                password: Optional[str] = None) -> Union[User, bool]:
    """Update a user 

    Args:
        data (Dict[str, Any]): the data to update
        db_obj (User): database object
        password (Optional[str], optional): the password passed in. Defaults to None.

    Returns:
        Union[User, bool]: Returns user object or a bool
    """
    user = crud_user.update(obj_in=data, db_obj=db_obj)
    if password:
        changed = crud_user.update_password(db_obj=user, password=password)
        if not changed:
            return False
    commit()
    return user


def get_email(n: Optional[int] = 0,
              action: Optional[int] = None,
              default: Optional[str] = None):
    """Request for email

    Args:
        n (Optional[int], optional): Reload count. Defaults to 0.
        action (Optional[int], optional): What type of email to collect. Defaults to None.
        default (Optional[str], optional): the default email. Defaults to None.

    Returns:
        [type]: [description]
    """
    if action == 2:
        email = typer.prompt(text="What is the new value", default=default)

    elif action == 1:
        email = typer.prompt(text="Input User Email")

    else:
        email = typer.prompt(text="Input New User Email")

    if not verify_email(email=email):
        n += 1
        return reload_echos(reload=True,
                            n=n,
                            func=get_email,
                            argument={
                                "n": n,
                                "default": default,
                                "action": action
                            })
    return email


def reload_echos(reload: bool,
                 n: int,
                 start_msg: Optional[str] = None,
                 func: Optional[Callable[..., Any]] = None,
                 argument: Optional[Dict[str, Any]] = None):
    """Reload Echos

    Args:
        reload (bool): if reload is accepted 
        n (int): No of reload done
        start_msg (Optional[str], optional): The first message. Defaults to None.
        func (Optional[Callable[..., Any]], optional): The fucntion that contains echo. Defaults to None.
        argument (Optional[Dict[str, Any]], optional): function arguement . Defaults to None.

    Raises:
        typer.Abort: abort the process
    """
    if reload:
        if n >= 3:
            typer.echo("Thats it! I am ending this")
            raise typer.Abort()
        typer.secho("Lets try that Again!",
                    fg=typer.colors.BLACK,
                    bg=typer.colors.WHITE)
        if func:
            func(**argument)
    else:
        if start_msg:
            typer.echo(start_msg)


def verify_email(email: str, check_exist: bool = False) -> bool:
    """Verify the email

    Args:
        email (str): The email to verify
        check_exist (bool, optional): check if email exist. Defaults to False.

    Returns:
        bool: True or False
    """
    try:

        email = EmailSchema(email=email)
    except ValidationError as e:
        error_dict = get_source_of_value_exception(e)
        loc = error_dict["loc"][0]
        msg = error_dict["msg"]
        typer.secho(f"The {loc} {msg}", fg=typer.colors.RED)
        return False
    if check_exist:
        user = crud_user.get_by_email(email=email.email)
        if user:
            typer.secho("User with email already exists", fg=typer.colors.RED)
            return False
    return True


def get_source_of_value_exception(value_exception: ValidationError) -> str:
    """Explain Error encountered

    Args:
        value_exception (ValidationError): Validation Error

    Returns:
        str: The error message
    """
    error_json = value_exception.json()
    error_dict = json.loads(error_json)[0]
    return error_dict


@db_session
def engine(
    num: int,
    level: int,
    data: Optional[Dict[str, Any]] = None,
    reload: bool = False,
    n: int = 0,
):
    """The Main Engine of the script

    Args:
        num (int): options number
        level (int): The option level
        data (Optional[Dict[str, Any]], optional): The previous data passed in. Defaults to None.
        reload (bool, optional): if engine should be reloaded . Defaults to False.
        n (int, optional): the number of reload. Defaults to 0.

    Returns:
        [type]: [description]
    """
    typer.secho("")
    if level == 1:
        if num == 1:
            reload_echos(reload=reload,
                         n=n,
                         start_msg="Initializing User Creation")
            n = 0
            email = get_email(n=n)
            if not verify_email(email=email, check_exist=True):
                return engine(num, level=level, reload=True, n=n + 1)
            name = typer.prompt(text="Input New User Name", type=str)
            password = typer.prompt(text="Input password for User",
                                    type=str,
                                    hide_input=True,
                                    confirmation_prompt=True)

            user = Register(**{
                "email": email,
                "name": name,
                "password": password
            })
            user = create_user(user=user)
            if not user:
                return engine(num, level=level, reload=True, n=n + 1)
            typer.secho(f"Sucessfully created new user: {user.uuid}",
                        fg=typer.colors.GREEN)
            typer.echo("")
            typer.echo("What would you want to do next?:")
            data = user.to_dict()

            return show_options(obj=AFTER_USER_CREATION, level=5, data=data)

        elif num == 2:
            reload_echos(reload=reload,
                         n=n,
                         start_msg="Initializing User Retrieval")
            n = 0
            email = get_email(n=n, action=1)

            if not verify_email(email=email):
                return engine(num, level=level, reload=True, n=n + 1)

            user = get_user_detail(email)
            user_dict: Dict[str, Any] = user.to_dict()
            typer.echo("Here are the user's details:")
            typer.echo("")

            for r in user_dict.keys():
                if r == "password":
                    continue
                typer.secho(f'{r}: {user_dict[r]}',
                            fg=typer.colors.BLUE,
                            nl=True)

            typer.echo('')
            typer.echo("What would you like to do with this user?:")

            return show_options(obj=PREMISES, level=2, data=user_dict)

    elif level == 2:
        if num == 1:
            reload_echos(reload=reload,
                         n=n,
                         start_msg="Initializing User Edit")
            user_keys = data.keys()
            new_values = {}
            password: Optional[str] = None

            for key in user_keys:
                cap_key = key.capitalize()

                if key == "id" or key == "uuid" or key == "date_created":
                    continue

                elif key == "password":
                    change = typer.confirm("Want to change the password?")
                    if not change:
                        continue
                    password = typer.prompt("Input new password",
                                            hide_input=True,
                                            confirmation_prompt=True)
                    continue
                elif key == "email":
                    typer.echo(f"Old value for {cap_key}: {data[key]}")
                    n = 0
                    email = get_email(n=n, action=2, default=data[key])
                    new_values[key] = email
                    continue

                elif key == "active":
                    typer.echo(f"Old value for {cap_key}: {data[key]}")
                    value = typer.prompt(text="What is the new value",
                                         default=data[key],
                                         type=bool)
                    new_values[key] = value
                    continue

                typer.echo(f"Old value for {cap_key}: {data[key]}")
                value = typer.prompt(text="What is the new value",
                                     default=data[key])
                new_values[key] = value

            old_email = data["email"]

            user = get_user_detail(email=old_email)

            user = update_user(data=new_values, password=password, db_obj=user)

            user_dict = user.to_dict()

            typer.secho(f"Sucessfully updated user: {user.uuid}",
                        fg=typer.colors.GREEN,
                        nl=True)

            typer.echo("What else would you like to do with this user")

            return show_options(obj=PREMISES, level=2, data=user_dict)

        elif num == 2:
            typer.echo("How would you like to add the premises?")
            return show_options(obj=ADD_PREMISE, level=3, data=data)

        elif num == 3:
            reload_echos(reload=reload,
                         n=n,
                         start_msg="Initializing Premise Removal")
            email = data["email"]
            user = get_user_detail(email=email)
            premises = user.premises
            if premises:
                for x in premises:
                    typer.echo(f'{x.name}: {x.uuid}')
                premises_uuid = typer.prompt("Input premises uuid")

                loc = crud_premises.get_by_uuid(uuid=premises_uuid)

                user.premises -= loc
                commit()

                typer.echo("Premises removed from user!")
                return show_options(obj=PREMISES, level=2, data=data)
            else:
                typer.secho("User not part of any premise",
                            fg=typer.colors.RED)
                return show_options(obj=PREMISES, level=2, data=data)

    elif level == 3:

        email = data["email"]
        user = get_user_detail(email=email)
        user_premises = user.premises
        no_of_premises = len(user_premises)

        typer.secho(f'User already has about {no_of_premises}',
                    fg=typer.colors.BRIGHT_BLUE,
                    nl=True)
        if no_of_premises > 0:
            typer.echo("Here are the details of the premises", nl=True)

        for premises in user_premises:
            typer.echo(f'uuid: {premises.uuid}')
            typer.echo(f'name : {premises.name}')
            typer.echo(f'manager name: {premises.manager.name}')

        if num == 1:
            reload_echos(reload=reload,
                         n=n,
                         start_msg="Initializing New Premises Creation")

            create_premises = typer.confirm(
                "Are you sure you want to create a new premises?")

            if not create_premises:
                typer.secho("Premises creation canceled",
                            fg=typer.colors.BRIGHT_RED)
                return show_options(obj=PREMISES, level=2, data=data)

            name = data["name"]

            typer.echo("Creating user as a manager")
            man = crud_manager.create(obj_in={"name": name, "email": email})

            new_premise_name = typer.confirm(
                "Want to input name for the premise?")

            if new_premise_name:
                name = typer.prompt("What is the new name of the premises")

            loc_data = {"name": name, "manager": man}

            loc = crud_premises.create(obj_in=loc_data)

            user.premises += loc

            commit()

            typer.secho(f"New premises created with the following {loc.uuid}",
                        fg=typer.colors.GREEN,
                        nl=True)

            typer.echo("Wanna create or add another premises?")

            return show_options(obj=ADD_PREMISE, level=3, data=data)

        elif num == 2:
            all_premises = crud_premises.get_multi()
            typer.secho("List of all of the premises present in the system",
                        fg=typer.colors.BLACK,
                        bg=typer.colors.WHITE)
            for premises in all_premises:
                typer.echo(f"{premises.name} : {premises.uuid}")

            premises_uuid = typer.prompt("Add user to what premises [uuid]",
                                         type=UUID4)

            user_premises = [x.uuid for x in user.premises]

            typer.echo("Checking if user already in premises", nl=True)

            with typer.progressbar(user_premises) as progress:
                for premises in progress:
                    if premises == premises_uuid:
                        typer.secho("User already part of that premises",
                                    fg=typer.colors.BRIGHT_RED)

                        typer.echo("Wanna try that again?")

                        return show_options(obj=ADD_PREMISE,
                                            level=3,
                                            data=data)

            typer.secho("User is not included in premises",
                        fg=typer.colors.BRIGHT_YELLOW)
            typer.secho("Adding user to premises ...",
                        fg=typer.colors.BRIGHT_YELLOW)

            the_premises = crud_premises.get_by_uuid(uuid=premises_uuid)
            user.premises += the_premises

            commit()

            typer.secho("Added User to Premises", fg=typer.colors.GREEN)

            typer.echo("Wanna try that again?")

            return show_options(obj=ADD_PREMISE, level=3, data=data)

        elif num == 3:
            return show_options(obj=PREMISES, level=2, data=data)

    elif level == 5:
        if num == 1:
            return engine(num=1, level=2, data=data)

        if num == 2:
            return engine(num=2, level=2, data=data)

        if num == 3:
            return engine(num=1, level=1)


def show_welcome_message():
    """Show the welcome message
    """
    typer.secho("User Management Cli v1.0", fg=typer.colors.BRIGHT_CYAN)
    typer.secho("")
    typer.echo("Hey There! What would you like to do today?")
    typer.secho("Below are the options we have for you:")


# Main Function
def main():
    create_all_tables()
    show_welcome_message()
    show_options()


if __name__ == "__main__":
    typer.run(main)