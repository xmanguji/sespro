from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pony.orm.core import desc
from pydantic import BaseModel
from pony.orm import select

from database import db

ModelType = TypeVar("ModelType", bound=db.Entity)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: ModelType) -> None:
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            model (ModelType): A Pony Entity class
        """
        self.model = model

    def get(self, *, id: Any) -> Optional[ModelType]:
        """Get data from database using the uuid

        Args:
            id (Any): the primarykey/identifier

        Returns:
            Optional[ModelType]: The Entity Object ( Pony Entity Class)
        """

        obj = self.model.get(id=id)

        return obj

    def get_by_uuid(self, *, uuid: str) -> Optional[ModelType]:
        """Get data from database using the uuid

        Args:
            id (Any): the primarykey/identifier

        Returns:
            Optional[ModelType]: The Entity Object ( Pony Entity Class)
        """

        obj = self.model.get(uuid=uuid)

        return obj

    def get_multi(
        self, *, limit: Optional[int] = None, sort_by: Optional[Dict] = None
    ) -> List[ModelType]:
        """Helps get multiple entiies from the database and retursn it as a list

        Args:
            limit (Optional[int], optional): the number of objects to return. Defaults to None.

        Returns:
            List[ModelType]: A list of entities
        """
        objs = select(obj for obj in self.model)

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                objs = objs.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                objs = objs.sort_by(sort_string)

        if limit:
            objs = objs.limit[:limit]
        else:
            objs = objs[:]

        return objs

    def create(self, *, obj_in: Union[CreateSchema, Dict[str, Any]]) -> ModelType:
        """Create or Store new data

        Args:
            obj_in (Union[CreateSchema, Dict[str, Any]]): the data to store

        Returns:
            ModelType: [description]
        """

        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data)

        return db_obj

    def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchema, Dict[str, Any]]
    ) -> ModelType:
        """Heps handle update of entities data

        Args:
            db_obj (ModelType): The Entity Object
            obj_in (Union[UpdateSchema, Dict[str, Any]]): the update data

        Returns:
            ModelType: [description]
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        db_obj = self.get_by_uuid(uuid=db_obj.uuid)
        db_obj.set(**update_data)

        return db_obj

    def remove(self, *, id: int) -> ModelType:

        obj = self.model.get(id=id)
        obj.delete()

        return obj

    def remove_by_uuid(self, *, uuid: str) -> ModelType:

        obj = self.model.get(uuid=uuid)

        obj.delete()

        return obj
