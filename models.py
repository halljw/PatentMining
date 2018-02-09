#!/usr/bin/env python

import numpy
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import hamming_loss
from sklearn.metrics import precision_recall_fscore_support

#####################################################################################################
# PART 1
# Train specified model
#####################################################################################################
def train_model(x, y, model):
    """
    Train model on expected input (x) and output (y)
    If no model is specified, Naive-Bayes is assumed.
    """
    if model=='NB':
        print("\tTraining NB model...")
        return OneVsRestClassifier(MultinomialNB()).fit(x, y)
    elif model=='SVM':
        print("\tTraining SVM model...")
        return OneVsRestClassifier(LinearSVC()).fit(x, y)
    elif model=='TREE':
        print("\tTraining decision tree model...")
        return OneVsRestClassifier(DecisionTreeClassifier()).fit(x, y)
    elif model=='MLP':                                                  # Multi-layer perceptron NN
        print("\tTraining neural net model...")
        return OneVsRestClassifier(MLPClassifier()).fit(x, y)
    elif model=='LOGREG':                                             
        print("\tTraining logistic regression model...")
        return OneVsRestClassifier(LogisticRegression()).fit(x, y)
    else:
        raise ValueError("train_model: invalid model selected")


#####################################################################################################
# PART 2
# Examine predicted labels and actual labels. Generate precision and recall,
# both overall and by section. Generate hamming loss.
#####################################################################################################
def calculate_hamming_loss(predictions, results):
    return numpy.mean([hamming_loss(pred, res) for pred, res in zip(predictions, results)])


def precision_recall(y_pred, y_true):
    """
    Given predicted values and actual values, evaluates a model.
    Evaluation conducted overall and by section. Returns overall prec and recall (micro 
    and macro), and lists of prec and recall by section.

    mic_prec, mic_rec, mic_f, mac_prec, mac_rec, mac_f, [precision_sections], [recall_sections], [f_sections]

    Micro: calcualte metrics globally by counting total true positives, false negatives, 
           and false positives
    Macro: claculate metrics for each label, find their unweighted mean.
    """
    micro_prec, micro_rec, micro_f, micro_ins = precision_recall_fscore_support(y_true, y_pred, average='micro')
    macro_prec, macro_rec, macro_f, macro_ins = precision_recall_fscore_support(y_true, y_pred, average='macro')
    precisions, recalls, fs, instances = precision_recall_fscore_support(y_true, y_pred)

    # If support for each label is not balanced (likely to be the case for D), possible to weight
    # by support. Uncomment below.
    #macro_prec, macro_rec, macro_f, macro_ins = precision_recall_fscore_support(y_true, y_pred, average='weighted')

    return micro_prec, micro_rec, micro_f, macro_prec, macro_rec, macro_f, precisions, recalls, fs
