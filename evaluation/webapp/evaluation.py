#!/usr/bin/python3
from datetime import datetime

import pdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics

from webapp import config, feature_strings

plt.rc('font', family='sans-serif')
plt.rc('font', serif='Helvetica Neue')


def weighted_f1(scores):
    f1_0 = scores["f1"][0] * scores["support"][0]
    f1_1 = scores["f1"][1] * scores["support"][1]
    return (f1_0 + f1_1) / (scores["support"][0] + scores["support"][1])


def plot_fp_tp_percent(eis_baseline, fpr, tpr, threshold_levels):

    fpr_plot, tpr_plot, threshold_plot = [], [], []

    false_pos_eis = eis_baseline[0, 1]
    true_pos_eis = eis_baseline[1, 1]

    for each_threshold in threshold_levels:
        threshold_plot.append(each_threshold * 100.)
        fpr_plot.append((fpr[each_threshold] - false_pos_eis)/false_pos_eis * 100.)
        tpr_plot.append((tpr[each_threshold] - true_pos_eis)/true_pos_eis * 100.)

    with plt.style.context(('ggplot')):
        plt.clf()
        fig, ax1 = plt.subplots()
        ax1.plot(threshold_plot, fpr_plot, "#000099")
        ax1.set_xlabel('threshold percent')
        ax1.set_ylabel('percent change in false positives', color="#000099")
        #plt.ylim([0.0, 100.0])
        ax2 = ax1.twinx()
        ax2.plot(threshold_plot, tpr_plot, "#CC0000")
        ax2.set_ylabel('percent change in true positives ', color="#CC0000")
        #plt.ylim([0.0, 100.0])
    plt.title("percent change in false and true positives for top x%")
    return fig


def plot_fp_tp_absolute(eis_baseline, fpr, tpr, threshold_levels):

    fpr_plot, tpr_plot, threshold_plot = [], [], []

    false_pos_eis = eis_baseline[0, 1]
    true_pos_eis = eis_baseline[1, 1]

    for each_threshold in threshold_levels:
        threshold_plot.append(each_threshold * 100.)
        fpr_plot.append(fpr[each_threshold] - false_pos_eis)
        tpr_plot.append(tpr[each_threshold] - true_pos_eis)

    with plt.style.context(('ggplot')):
        plt.clf()
        fig, ax1 = plt.subplots()
        ax1.plot(threshold_plot, fpr_plot, "#000099")
        ax1.set_xlabel('threshold percent')
        ax1.set_ylabel('change in number of false positives', color="#000099")
        ax2 = ax1.twinx()
        ax2.plot(threshold_plot, tpr_plot, "#CC0000")
        ax2.set_ylabel('change in number of true positives ', color="#CC0000")
    plt.title("absolute change in false and true positives for top x%")
    return fig


def plot_fp_tp_absolute_nothresh(eis_baseline, fpr, tpr, threshold_levels):

    fpr_plot, tpr_plot, threshold_plot = [], [], []

    false_pos_eis = eis_baseline[0, 1]
    true_pos_eis = eis_baseline[1, 1]

    for each_threshold in threshold_levels:
        threshold_plot.append(each_threshold * 100.)
        fpr_plot.append(fpr[each_threshold] - false_pos_eis)
        tpr_plot.append(tpr[each_threshold] - true_pos_eis)

    with plt.style.context(('ggplot')):
        plt.clf()
        fig, ax1 = plt.subplots()
        ax1.plot(tpr_plot, fpr_plot)
        ax1.plot(tpr_plot, fpr_plot, 'o-')
        for ind, label in enumerate(threshold_levels):
            ax1.annotate('top {}%'.format(int(label*100)), xy=(tpr_plot[ind], fpr_plot[ind]))
        ax1.set_xlabel('change in number of true positives')
        ax1.set_ylabel('change in number of false positives')
    plt.title("tradeoff in absolute change in false and true positives")
    return fig


def plot_fp_tp_percent_nothresh(eis_baseline, fpr, tpr, threshold_levels):

    fpr_plot, tpr_plot, threshold_plot = [], [], []

    false_pos_eis = eis_baseline[0, 1]
    true_pos_eis = eis_baseline[1, 1]

    for each_threshold in threshold_levels:
        threshold_plot.append(each_threshold * 100.)
        fpr_plot.append((fpr[each_threshold] - false_pos_eis)/false_pos_eis * 100.)
        tpr_plot.append((tpr[each_threshold] - true_pos_eis)/true_pos_eis * 100.)

    with plt.style.context(('ggplot')):
        plt.clf()
        fig, ax1 = plt.subplots()
        ax1.plot(tpr_plot, fpr_plot, 'o-')
        for ind, label in enumerate(threshold_levels):
            ax1.annotate('top {}%'.format(int(label*100)), xy=(tpr_plot[ind], fpr_plot[ind]))
        ax1.set_xlabel('percent change in true positives')
        ax1.set_ylabel('percent change in false positives')
    plt.title("tradeoff in percent change in false and true positives")
    return fig


def plot_normalized_confusion_matrix(labels, predictions):
    cutoff = 0.5
    #predictions_binary = np.copy(predictions)
    #predictions_binary[predictions_binary >= cutoff] = 1
    #predictions_binary[predictions_binary < cutoff] = 0
    predictions_binary = [ 1 if x > cutoff_probability else 0 for x in predictions ]

    cm = metrics.confusion_matrix(labels, predictions_binary)
    np.set_printoptions(precision=2)
    fig = plt.figure()
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    target_names = ["No adverse inc.", "Adverse inc."]
    plt.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Normalized Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig


def plot_confusion_matrix_at_x_proportion(labels, predictions, x_proportion):

    cutoff_index = int(len(predictions) * x_proportion)
    cutoff_index = min(cutoff_index, len(predictions) - 1)

    sorted_by_probability = np.sort(predictions)[::-1]
    cutoff_probability = sorted_by_probability[cutoff_index]

    #predictions_binary = np.copy(predictions)
    #predictions_binary[predictions_binary >= cutoff_probability] = 1
    #predictions_binary[predictions_binary < cutoff_probability] = 0
    predictions_binary = [ 1 if x > cutoff_probability else 0 for x in predictions ]

    cm = metrics.confusion_matrix(labels, predictions_binary)
    np.set_printoptions(precision=2)
    fig = plt.figure()

    target_names = ["No adverse inc.", "Adverse inc."]
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig


def plot_normalized_confusion_matrix_at_x_proportion(labels, predictions, x_proportion):

    cutoff_index = int(len(predictions) * x_proportion)
    cutoff_index = min(cutoff_index, len(predictions) - 1)

    sorted_by_probability = np.sort(predictions)[::-1]
    cutoff_probability = sorted_by_probability[cutoff_index]

    #predictions_binary = np.copy(predictions)
    #predictions_binary[predictions_binary >= cutoff_probability] = 1
    #predictions_binary[predictions_binary < cutoff_probability] = 0
    predictions_binary = [ 1 if x > cutoff_probability else 0 for x in predictions ]

    cm = metrics.confusion_matrix(labels, predictions_binary)
    np.set_printoptions(precision=2)
    fig = plt.figure()
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    target_names = ["No adverse inc.", "Adverse inc."]
    plt.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Normalized Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig


def humanize_names(feature_names):
    human_readable = []

    for name in feature_names:
        try:
            human_readable.append(feature_strings.mapping[name])
        except:
            human.readable.append(name)

    return human_readable


def plot_feature_importances(feature_names, feature_importances, N=30):
    #humanized_featnames = humanize_names(feature_names)
    humanized_featnames = feature_names

    importances = list(zip(humanized_featnames, list(feature_importances)))
    importances = pd.DataFrame(importances, columns=["Feature", "Importance"])
    importances = importances.set_index("Feature")

    # Sort by the absolute value of the importance of the feature
    importances["sort"] = abs(importances["Importance"])
    importances = importances.sort(columns="sort", ascending=False).drop("sort", axis=1)
    importances = importances[0:N]

    # Show the most important positive feature at the top of the graph
    importances = importances.sort(columns="Importance", ascending=True)

    with plt.style.context(('ggplot')):
        fig, ax = plt.subplots(figsize=(16,12))
        ax.tick_params(labelsize=16)
        importances.plot(kind="barh", legend=False, ax=ax)
        ax.set_frame_on(False)
        ax.set_xlabel("Importance", fontsize=20)
        ax.set_ylabel("Feature", fontsize=20)
    plt.tight_layout()
    plt.title("Top Feature Importances", fontsize=20).set_position([.5, 0.99])
    return fig


def plot_growth(results):
    results = pd.DataFrame(results, columns=["date", "score"])
    results = results.set_index("date")
    results["score"] = results["score"].astype(float)
    results = results.reindex(pd.date_range(datetime(2015, 10, 1),
                                            datetime(2016, 3, 1)))
    # results["random"] = pd.Series(3409/float(6124), index=results.index)
    with plt.style.context(('ggplot')):
        fig, ax = plt.subplots(figsize=(8, 3))
        results["score"].plot(legend=False, ax=ax, marker="x")
        results["random"].plot(legend=False, ax=ax, style='--')

    ax.set_ylabel(config.score_name)
    plt.tight_layout()
    ax.set_ylim(0.5, 1.0)
    return fig


def fpr_tpr(labels, predictions, x_proportion):
    cutoff_index = int(len(predictions) * x_proportion)
    cutoff_index = min(cutoff_index, len(predictions) - 1)

    sorted_by_probability = np.sort(predictions)[::-1]
    cutoff_probability = sorted_by_probability[cutoff_index]

    #predictions_binary = np.copy(predictions)
    #predictions_binary[predictions_binary >= cutoff_probability] = 1
    #predictions_binary[predictions_binary < cutoff_probability] = 0
    predictions_binary = [ 1 if x > cutoff_probability else 0 for x in predictions ]

    return metrics.confusion_matrix(labels, predictions_binary)


def precision_at_x_proportion(test_labels, test_predictions, x_proportion=0.01,
                           return_cutoff=False):

    cutoff_index = int(len(test_predictions) * x_proportion)
    cutoff_index = min(cutoff_index, len(test_predictions) - 1)

    sorted_by_probability = np.sort(test_predictions)[::-1]
    cutoff_probability = sorted_by_probability[cutoff_index]

    #test_predictions_binary = np.copy(test_predictions)
    #test_predictions_binary[test_predictions_binary >= cutoff_probability] = 1
    #test_predictions_binary[test_predictions_binary < cutoff_probability] = 0
    test_predictions_binary = [ 1 if x > cutoff_probability else 0 for x in test_predictions ]

    precision, _, _, _ = metrics.precision_recall_fscore_support(
        test_labels, test_predictions_binary)
    precision = precision[1]  # only interested in precision for label 1

    if return_cutoff:
        return precision, cutoff_probability
    else:
        return precision


def recall_at_x_proportion(test_labels, test_predictions, x_proportion=0.01,
                        return_cutoff=False):

    cutoff_index = int(len(test_predictions) * x_proportion)
    cutoff_index = min(cutoff_index, len(test_predictions) - 1)

    sorted_by_probability = np.sort(test_predictions)[::-1]
    cutoff_probability = sorted_by_probability[cutoff_index]

    #test_predictions_binary = np.copy(test_predictions)
    #test_predictions_binary[test_predictions_binary >= cutoff_probability] = 1
    #test_predictions_binary[test_predictions_binary < cutoff_probability] = 0
    test_predictions_binary = [ 1 if x > cutoff_probability else 0 for x in test_predictions ]

    _, recall, _, _ = metrics.precision_recall_fscore_support(
        test_labels, test_predictions_binary)
    recall = recall[1]  # only interested in precision for label 1

    if return_cutoff:
        return recall, cutoff_probability
    else:
        return recall


def plot_precision_recall_n(test_labels, test_predictions):
    y_score = test_predictions
    precision_curve, recall_curve, pr_thresholds = \
        metrics.precision_recall_curve(test_labels, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score >= value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)

    with plt.style.context(('ggplot')):
        plt.clf()
        fig, ax1 = plt.subplots()
        ax1.plot(pct_above_per_thresh, precision_curve, "#000099")
        ax1.set_xlabel('proportion of population')
        ax1.set_ylabel('precision', color="#000099")
        plt.ylim([0.0, 1.0])
        ax2 = ax1.twinx()
        ax2.plot(pct_above_per_thresh, recall_curve, "#CC0000")
        ax2.set_ylabel('recall', color="#CC0000")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
    plt.title("Precision-recall at x-proportion")
    return fig


def plot_precision_cutoff(test_labels, test_predictions):
    percent_range = [0.001 * i for i in range(1, 10)] + \
        [0.01 * i for i in range(1, 101)]
    precisions_and_cutoffs = [precision_at_x_proportion(
        test_labels, test_predictions, x_proportion=p, return_cutoff=True)
                              for p in percent_range]
    precisions, cutoffs = zip(*precisions_and_cutoffs)

    with plt.style.context(('ggplot')):
        fig, ax = plt.subplots()
        ax.plot(percent_range, precisions, "#000099")
        ax.set_xlabel('proportion of population')
        ax.set_ylabel('precision', color="#000099")
        plt.ylim([0.0, 1.0])
        ax2 = ax.twinx()
        ax2.plot(percent_range, cutoffs,  "#CC0000")
        ax2.set_ylabel('cutoff at', color="#CC0000")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
    plt.title("Precision at x-proportion")
    return fig


def plot_ROC(test_labels, test_predictions):
    fpr, tpr, thresholds = metrics.roc_curve(
        test_labels, test_predictions, pos_label=1)
    auc = "%.2f" % compute_AUC(test_labels, test_predictions)
    title = 'ROC Curve, AUC = '+str(auc)
    with plt.style.context(('ggplot')):
        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, "#000099", label='ROC curve')
        ax.plot([0, 1], [0, 1], 'k--', label='Baseline')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc='lower right')
        plt.title(title)
    return fig


def compute_AUC(test_labels, test_predictions):
    fpr, tpr, thresholds = metrics.roc_curve(
        test_labels, test_predictions, pos_label=1)
    return metrics.auc(fpr, tpr)
