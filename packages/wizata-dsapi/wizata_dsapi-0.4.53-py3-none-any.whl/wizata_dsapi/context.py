import uuid
import pandas

from .mlmodel import MLModel
from .plot import Plot
from .ilogger import ILogger
from .api_interface import ApiInterface
from .pipeline import PipelineStep

from .mlmodel import MLModelConfig
from .script import ScriptConfig

from .template import Template
from .twinregistration import TwinRegistration

from datetime import datetime


class Context(ILogger):
    """
    Context defines all properties, dataframes, models and other data passed through pipeline steps.
    - properties are accessible on properties property.
    - output dataframe(s) use return statement.
    - input dataframe(s) get them by parameters or use dataframe property directly.
    - for model use the set_model statement : support only one model per script.
    - for plot use the set_model statement : support only one plot per script.
    - dataframes, models and additional plots used within the pipelines can also be accessed, read-only.
    """

    def __init__(self,
                 pipeline_id: uuid.UUID = None,
                 execution_id: uuid.UUID = None,
                 template: Template = None,
                 registration: TwinRegistration = None,
                 now: datetime = None,
                 step: PipelineStep = None):
        self.pipeline_id = pipeline_id
        self.execution_id = execution_id
        self.template = template
        self.registration = registration
        self.now = now
        self.step = step

        self.models = {}
        self.dataframes = {}
        self.datapoints = {}
        self.properties = {}
        self.plots = {}

        self._logger = None

        self.__key_mapping = None
        self.__primary_key = None
        self.__temporary_dataframe = None

        self.__new_plot = None
        self.__new_model = None

        self.grafana_api = None
        self.config = None

        self._api = None

    def write_log(self, message: str, level: int = 7):
        """
        write log in console (only in experiment mode) - if running locally it will print in the console.
        :param message: message to write.
        :param level: from 7=DEBUG, 6=INFO, 3=ERROR to 1=CRITICAL
        """
        if self._logger is None:
            print(message)
        else:
            self._logger.write_log(message=message, level=level)

    @property
    def api(self) -> ApiInterface:
        """
        Accessible DS API functionalities within runner context.
        """
        return self._api

    @api.setter
    def api(self, api: ApiInterface):
        self._api = api

    @property
    def dataframe(self):
        """
        dataframe - use for single input only - for output use return statement
        """
        if self.__primary_key is not None and self.__key_mapping is not None and self.__primary_key in self.__key_mapping and self.__key_mapping[self.__primary_key] in self.dataframes:
            return self.dataframes[self.__key_mapping[self.__primary_key]]
        elif self.__temporary_dataframe is not None:
            return self.__temporary_dataframe
        else:
            return None

    @dataframe.setter
    def dataframe(self, df: pandas.DataFrame):
        if self.__primary_key is not None and self.__key_mapping is not None and self.__primary_key in self.__key_mapping and self.__key_mapping[self.__primary_key] in self.dataframes:
            self.dataframes[self.__key_mapping[self.__primary_key]] = df
        else:
            self.__temporary_dataframe = df

    def append(self, key: str, obj, overwrite: bool = True):
        """
        append an object (pandas.Dataframe or any properties)
        :param key: dictionary identifier - name inside your pipeline.
        :param obj: ML Model, Dataframe or any properties (must be JSON serializable type).
        :param overwrite: by default - allow modifying an existing object. can be set to false.
        """
        if key is None or key == "":
            raise KeyError('please provide a non empty key.')

        if isinstance(obj, pandas.DataFrame):
            if not overwrite and key in self.dataframes:
                raise KeyError(f'cannot overwrite existing dataframe in context with key {key}')
            self.dataframes[key] = obj
        else:
            if not overwrite and key in self.properties:
                raise KeyError(f'cannot overwrite existing properties in context with key {key}')
            self.properties[key] = obj

    def get(self, key: str):
        """
        get key from either dataframes, models, plots or properties.
        return None if not found.
        """
        if key in self.dataframes:
            return self.dataframes[key]
        elif key in self.models:
            return self.models[key]
        elif key in self.plots:
            return self.plots[key]
        elif key in self.properties:
            return self.properties[key]
        else:
            return None

    def set_plot(self, figure, name="Unkwown"):
        """
        set plot to be added to the context.
        :param figure: Plotly figure.
        :param name: Name of the plot.
        :return: Plot object prepared.
        """
        plot = Plot()
        plot.name = name
        plot.figure = figure
        self.__new_plot = plot
        return plot

    def get_plot(self) -> Plot:
        """
        get plot set to be added to the context.
        """
        return self.__new_plot

    def set_model(self, trained_model, input_columns, output_columns=None, has_anomalies=False, scaler=None):
        """
        set model to be added to the context.
        :param trained_model: Trained Model to be stored as a pickled object.
        :param input_columns: List of str defining input columns to call the model (df.columns)
        :param output_columns: List of output columns - Optional as can be detected automatically during validation.
        :param has_anomalies: False by default, define if the model set anomalies
        :param scaler: Scaler to be stored if necessary.
        :return: ML Model object prepared.
        """
        ml_model = MLModel()
        ml_model.trained_model = trained_model
        ml_model.scaler = scaler
        ml_model.input_columns = input_columns
        ml_model.output_columns = output_columns
        ml_model.has_anomalies = has_anomalies
        self.__new_model = ml_model
        return ml_model

    def get_model(self) -> MLModel:
        """
        get model to be added to the context.
        """
        return self.__new_model

    def reset(self):
        """
        reset context between step execution - remove all step info, but keep all data.
        """
        self.__new_plot = None
        self.__new_model = None
        self.__key_mapping = None
        self.__primary_key = None
        self.__temporary_dataframe = None
        self.step = None

    def _set_mapping(self, key_mapping: dict, primary_key: str):
        """
        set step mapping between pipeline names and step name
        """
        self.__key_mapping = key_mapping
        self.__primary_key = primary_key

    def current_dataframes(self) -> dict:
        """
        current dataframes a dictionary with all current named dataframes specific for this script.
        dataframes contains all accessible dataframes for the pipeline mapped.
        single dataframe context is accessible with context.dataframe and is not named
        """
        dataframes = {}
        if self.__key_mapping is not None:
            for key in self.__key_mapping:
                dataframes[self.__key_mapping[key]] = self.dataframes[key]
        return dataframes

    def get_script_config(self) -> ScriptConfig:
        """
        extract script configuration from the context.
        """
        if self.step is None:
            raise ValueError(f'there is no step defined in the context.')
        if self.step.config is None:
            raise ValueError(f'there is no step config defined in the context.')
        if not isinstance(self.step.config, ScriptConfig):
            raise TypeError(f'step is not configured as a script/plot step')
        return self.step.config

    def get_model_config(self) -> MLModelConfig:
        """
        extract model configuration from the context.
        """
        if self.step is None:
            raise ValueError(f'there is no step defined in the context.')
        if self.step.config is None:
            raise ValueError(f'there is no step config defined in the context.')
        if not isinstance(self.step.config, MLModelConfig):
            raise TypeError(f'step is not configured as a model step')
        return self.step.config
