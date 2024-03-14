from enum import Enum
import pandas as pd
import json
from .metrics.regression import __ALL__ as r__ALL__
from .metrics.classification import __ALL__ as c__ALL__
from .metrics.regression import *
from .metrics.classification import *
import loguru


"""
Each function written in this .py 
file is necessary control functions for the parameters taken by the info classes in _request.py.
"""

reg = ["SVR",
"BaggingRegressor",
"NuSVR",
"RandomForestRegressor",
"XGBRegressor",
"GradientBoostingRegressor",
"ExtraTreesRegressor",
"AdaBoostRegressor",
"HistGradientBoostingRegressor",
"PoissonRegressor",
"LGBMRegressor",
"KNeighborsRegressor",
"DecisionTreeRegressor",
"MLPRegressor",
"HuberRegressor",
"GammaRegressor",
"LinearSVR",
"RidgeCV",
"BayesianRidge",
"Ridge",
"TransformedTargetRegressor",
"LinearRegression",
"ElasticNetCV",
"LassoCV",
"LassoLarsIC",
"LassoLarsCV",
"Lars",
"LarsCV",
"SGDRegressor",
"TweedieRegressor",
"GeneralizedLinearRegressor",
"ElasticNet",
"Lasso",
"RANSACRegressor",
"OrthogonalMatchingPursuitCV",
"PassiveAggressiveRegressor",
"GaussianProcessRegressor",
"OrthogonalMatchingPursuit",
"ExtraTreeRegressor",
"DummyRegressor",
"LassoLars",
"KernelRidge",
"CatBoostRegressor",
"MLPRegressor",
"ELM"]

cls = ["LinearSVC",
"SGDClassifier",
"MLPClassifier",
"XGBClassifier",
"Perceptron",
"LogisticRegression",
"LogisticRegressionCV",
"SVC",
"CalibratedClassifierCV",
"PassiveAggressiveClassifier",
"LabelPropagation",
"LabelSpreading",
"RandomForestClassifier",
"GradientBoostingClassifier",
"QuadraticDiscriminantAnalysis",
"HistGradientBoostingClassifier",
"RidgeClassifierCV",
"RidgeClassifier",
"AdaBoostClassifier",
"ExtraTreesClassifier",
"KNeighborsClassifier",
"BaggingClassifier",
"BernoulliNB",
"LinearDiscriminantAnalysis",
"GaussianNB",
"NuSVC",
"DecisionTreeClassifier",
"NearestCentroid",
"ExtraTreeClassifier",
"CheckingClassifier",
"DummyClassifier",
"CatBoostClassifier",
"MLPClassifier",
"LGBMClassifier"]

scalers =["minmax","standard","maxabs","robust"]
#class period(Enum):
#    montly     = 'Montly'
#    daily      = 'Daily'
#    weekly     = "Weekly"
#    hourly     = 'Hourly'
#    thirtymin  = '30min'
#    fifteenmin = "15min"
#    tenmin     = "10min"
#    fivemin    = "5min"
#    onemin     = "1min"
#
#
#def _periods(period_):
#
#    """
#    It controls the period values taken as parameters.
#    :param period_: 'montly','daily','weekly','hourly','30min','15min','10m','5min','1min'
#    :return:
#    """
#    if period_.lower() == "montly":
#        if period.daily.value != period_ and period.daily.value != period_.lower() and \
#                period.daily.value != period_.upper() and period.daily.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "daily":
#        if period.daily.value != period_ and period.daily.value != period_.lower() and \
#                period.daily.value != period_.upper() and period.daily.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "weekly":
#        if period.weekly.value != period_ and period.weekly.value != period_.lower() and \
#                period.weekly.value != period_.upper() and period.weekly.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "hourly":
#        if period.hourly.value != period_ and period.hourly.value != period_.lower() and \
#                period.hourly.value != period_.upper() and period.hourly.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "30min":
#        if period.thirtymin.value != period_ and period.thirtymin.value != period_.lower() and \
#                period.thirtymin.value != period_.upper() and period.thirtymin.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "15min":
#        if period.fifteenmin.value != period_ and period.fifteenmin.value != period_.lower() and \
#                period.fifteenmin.value != period_.upper() and period.fifteenmin.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "10min":
#        if period.tenmin.value != period_ and period.tenmin.value != period_.lower() and \
#                period.tenmin.value != period_.upper() and period.tenmin.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "5min":
#        if period.fivemin.value != period_ and period.fivemin.value != period_.lower() and \
#                period.fivemin.value != period_.upper() and period.fivemin.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#    elif period_.lower() == "1min":
#        if period.onemin.value != period_ and period.onemin.value != period_.lower() and \
#                period.onemin.value != period_.upper() and period.onemin.value != period_.capitalize():
#            raise ValueError('Not a valid period.')
#


def check_period( dataFrame: pd.DataFrame) -> str:
    a = dataFrame.index[1] - dataFrame.index[0]
    if a.components.days == 1:
        return "Daily"
    elif a.components.days == 7:
        return "Weekly"
    elif a.components.days >= 25:
        return "Montly"
    elif a.components.days == 0 and a.components.hours == 1:
        return "Hourly"
    elif a.components.days == 0 and a.components.hours == 0 and a.components.minutes == 30:
        return "30min"
    elif a.components.days == 0 and a.components.hours == 0 and a.components.minutes == 15:
        return "15min"
    elif a.components.days == 0 and a.components.hours == 0 and a.components.minutes == 10:
        return "10min"
    elif a.components.days == 0 and a.components.hours == 0 and a.components.minutes == 5:
        return "5min"
    elif a.components.days == 0 and a.components.hours == 0 and a.components.minutes == 1:
        return "1min"


def check(targetCol):
    if bool(targetCol) is False:
        raise AttributeError("type object '_info' has no attribute 'targetCol' : {}".format(targetCol))

#def check_period(period):
#    if period.lower() in ('montly'
#                          'daily'
#                          "weekly"
#                          'hourly'
#                          '30min'
#                          "15min"
#                          "10min"
#                          "5min"
#                          "1min"):
#        return True
#    else:
#        raise ValueError(f'Not a valid period: ("montly",'
#                         f' "daily", "weekly", "hourly", "30min",'
#                         f'"15min", "10min","5min", "1min",{period}')


def evaluate(metric):
    """
    :param metric:
    :return:
    """
    err = {"reg" : False,
           "cls" : False
           }
    if metric not in [x for x in r__ALL__.keys().__iter__()] \
            and metric not in [x for x in r__ALL__.values().__iter__()]:
        err["reg"] = False
    else:err["reg"] = True
    if metric not in [x for x in c__ALL__.keys().__iter__()] \
            and metric not in [x for x in c__ALL__.values().__iter__()]:
        err["cls"] = False
    else:err["cls"] = True
    if (err["reg"] is False and err["cls"] is False):
        return ValueError(f'You entered {metric}, "modelName" should be parameters  : '
                        f'" Classification metrics : {json.dumps(c__ALL__)}" '
                          f'or Regression metrics : {json.dumps(r__ALL__)}')
    else:
        r__ALL__.update(c__ALL__)
        for i,j in r__ALL__.items():
            if i == metric or j == metric:
                return i,eval(i)
def check_M_modelname(modelname,auto=False):
    """
    :param modelname:
    :param auto:
    :return:
    """
    if isinstance(modelname, str):
        if auto is False:
            for r in reg:
                if modelname.lower() == r.lower():
                    return r
            for c in cls:
                if modelname.lower() == c.lower():
                    return c
            if modelname.lower() != c.lower() or modelname.lower() != r.lower():
                raise ValueError(f'You entered {modelname}, "modelName" should be parameters  : '
                        f'"{reg,cls}"')

def check_S_modelname(modelname):
    """
    :param modelname:
    :return:
    """
    if isinstance(modelname, str):
        if modelname.lower() not in ("arima","sarima"):
            raise ValueError(f'You entered {modelname}, "modelName" should be parameters  : '
                             f'"arima or sarima"')



def check_D_modelname(modelname):
    """
    :param layers:
    :param modelname:
    :return:
    """
    if isinstance(modelname, str):
        if modelname.lower() not in ("rnn", "lstm", "bilstm", "convlstm", "tcn", "lstnet"):
            raise ValueError(f'You entered {modelname}, "modelName" should be parameters  : '
                             f'"rnn","lstm","bilstm","convlstm","lstnet" or "tcn"')
    else:
        raise TypeError(f"Argument save must be of type bool, not {type(modelname)}")

    # if modelname == "lstnet":
    #     if layers["Layer"]["unit"].__len__() != 3 or \
    #             layers["Layer"]["activation"].__len__() != 3 or \
    #             layers["Layer"]["dropout"].__len__() != 3:
    #         raise AttributeError(f'your entered {modelname},'
    #                              f' If modelname lstnet is entered, you cannot change layers.')



def check_layer(layer, info):
    """
    :param layer: a dictionary of layer parameters
    :param info: an object with modelname attribute
    :return: None
    """
    try:
        if isinstance(layer, dict):
            for key in layer.keys(): # use keys instead of values
                if isinstance(layer[key], list): # use layer[key] to access the value
                    for k in layer[key]:
                        if type(k) != int and key == "unit":
                            raise TypeError(f'must be int not {type(k)}')
                        elif type(k) != str and key == "activation":
                            raise TypeError(f'must be str not {type(k)}')
                        elif type(k) != float and key == "dropout":
                            raise TypeError(f'must be float not {type(k)}')
                        continue
                else:
                    raise TypeError("must be list")
            # check the length of values
            if len(layer["unit"]) != len(layer["activation"]):
                raise ValueError("units and activation are not equal")
            if len(layer["unit"]) != len(layer["dropout"]):
                raise ValueError("units and dropout are not equal")
        info.dict_ = layer

        loguru.logger.info(f'The model selected is "{info.modelname.upper()}"!')
    except TypeError as e: # specify the error type
        loguru.logger.error(e) # log the error message
        loguru.logger.info("The model selected is LSTNET!")

#def check_layer(layer,info):
#    """
#    :param layer:
#    :param info:
#    :return:
#    """
#    try:
#        if isinstance(layer, dict):
#            for key in layer.keys():
#                if key == "Layer":
#                    for key in layer.values():
#                        if isinstance(key["unit"], list):
#                            for k in key["unit"]:
#                                if type(k) != int:
#                                    raise TypeError(f'must be int not {type(k)}')
#                                continue
#                            for k in key["activation"]:
#                                if type(k) != str:
#                                    raise TypeError(f'must be str not {type(k)}')
#                                continue
#                            for k in key["dropout"]:
#                                if type(k) != float:
#                                    raise TypeError(f'must be float not {type(k)}')
#                                continue
#                        else:
#                            raise TypeError("must be list")
#                else:
#                    layer = {"Layer": layer[key]}
#        info.dict_ = layer
#    except:
#        loguru.logger.info("The model selected is LSTNET!")

def check_scaler(scaler):
    """
    :param scaler:
    :return:
    """
    if scaler is not None:
        if scaler not in scalers:
            raise ValueError(f'You entered {scaler}, "scaler" should be parameters  : '
                             f'"minmax,standard,maxabs or robust"')
def check_date_in_data(dataFrame: pd.DataFrame, date: str):
    if bool(date):
        if dataFrame[dataFrame.index == date].__len__()==0:
            raise ValueError(
                f'The date entered was not found., {date}')

def check_forecast_date(dataFrame: pd.DataFrame, info):
    check_date_in_data(dataFrame,info.forecastingStartDate)
    #Forecasting
    if bool(info.forecastingStartDate) is False and bool(info.forecastNumber) is True:
        info.forecastingStartDate = str(dataFrame.index[-1])
    elif bool(info.forecastingStartDate) is False and bool(info.forecastNumber) is False:
        info.forecastingStartDate = str(dataFrame.index[-1])
        info.forecastNumber = 24
    elif bool(info.forecastingStartDate) is True and bool(info.forecastNumber) is False:
        if dataFrame[dataFrame.index > info.forecastingStartDate].__len__() != 0:
            info.forecastNumber = dataFrame[dataFrame.index > info.forecastingStartDate].__len__()
        else:
            info.forecastNumber = 24
    elif bool(info.forecastingStartDate) is True and bool(info.forecastNumber) is True:
        if info.forecastNumber > \
                dataFrame[dataFrame.index > info.forecastingStartDate].__len__() and dataFrame[dataFrame.index > info.forecastingStartDate].__len__() != 0:
            info.forecastNumber = \
                dataFrame[dataFrame.index > info.forecastingStartDate].__len__()



       # raise TypeError \
        #    (f"Argument save must be of type int, not {type(info.forecastNumber)}")



