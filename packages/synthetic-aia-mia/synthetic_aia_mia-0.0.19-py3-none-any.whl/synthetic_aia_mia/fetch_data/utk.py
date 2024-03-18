"""Downlaod and manages train / test split for UTKFaces dataset."""

from sklearn.model_selection import StratifiedKFold
import aia_fairness.dataset_processing as dp

from . import split

def load(sensitive=[],k=0):
    """Load UTKFaces Dataset. Downloads if data are not available. 

    :param k: (Optinal default=0) Corss validation step in {0,1,2,3,4}.
    :type k: int
    :param sensitive: (Optional default=[]) List of sensitive attributes to include in the features. The sensitive attribute are "sex" and "race".
    :type sensitive: list of str
    :return: Train and test split numpy.ndarray in a dictionary.
    :rtype: Doctionary
    """
    def loop(sensitive):
        data = {}
        if sensitive == []:
                tmp = dp.load_format("UTK", "sex")
                data["x"] = tmp["x"]
                data["y"] = tmp["y"]

        else:
            for s in sensitive:
                tmp = dp.load_format("UTK", s)
                data["x"] = tmp["x"]
                data["y"] = tmp["y"]
                data[s] = tmp["z"]

        return data

    try:
        data = loop(sensitive)
    except:
        print("Downloading UTk")
        dp.load_utk()
        data = loop(sensitive)


    skf = StratifiedKFold(random_state=1234,shuffle=True)
    
    for i,(tmp_train,tmp_test) in enumerate(skf.split(data["x"],data["y"])):
        if i==k:
            train = tmp_train
            test = tmp_test
    data_split = {"train":{},"test":{}}
    if sensitive==[]:
        data_split["train"] = {"x":data["x"][train],
                        "y":data["y"][train]}
        data_split["test"] = {"x":data["x"][test],
                        "y":data["y"][test]}
    else:
        for s in sensitive:
            data_split["train"][s] = data[s][train]
            data_split["test"][s] = data[s][test]

    return data_split



