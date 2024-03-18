

import os

from sqlalchemy import create_engine
from alchemyrohan.meta_data import MetaDataHolder
from alchemyrohan.wizard import *


__all__ = ['assemble_models']


class AlchemyRohanModuleError(Exception): ...


def assemble_models(
	db_creds: str, 
	table_names: list,
    abs_path_to_models: str = None,
    py_path_to_model: str = None
	) -> None:
    """
    Creates database models for SqlAlchemy.

    Args:
        db_creds (str): Credential string to connect to the database.
        table_names (list): Names of the tables.
        abs_path_to_models (str, optional): Absolute path to the location
            where the created models will be saved. Defaults to the 
            current directory.
        py_path_to_model (str, optional): Pythonic path to the models in 
        the project. For example, 'project_name.db.models'. This will be 
        written in code as: 
        'from project_name.db.models.TableName import TableName'.

    Returns:
        None 

    Raises:
        AlchemyRohanPathError: _description_
        AlchemyRohanDatabaseError: _description_
        AlchemyRohanGenerateModelError: _description_

    """

    if not abs_path_to_models:
        abs_path_to_models = os.getcwd()
    elif not os.path.isdir(abs_path_to_models):
        raise AlchemyRohanPathError(
            f'This path does not exist: {abs_path_to_models}'
            )
    if not py_path_to_model:
        py_path_to_model = 'py_path_to_model'
    
    engine = create_engine(db_creds)
    for table in table_names:
        code_holder = generate_code(MetaDataHolder(
            engine,
            table
            ),
            py_path_to_model
            )
        model_template = construct_model(code_holder)
        generate_model(
            table,
            model_template,
            abs_path_to_models
            )

        generate_init_file(
            table,
            abs_path_to_models,
            py_path_to_model
        )




    