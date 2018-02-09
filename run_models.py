#!/usr/bin/env python

import os, sys, time, pickle
from make_data import *
from models import *

def output_results(results, model, N, tier, analysis):
    if not os.path.exists('{}_Results/{}'.format(tier, analysis)):
        os.makedirs('{}_Results/{}'.format(tier, analysis))
    title = "{}_{}".format(model, N)
    with open('{}_Results/{}/{}'.format(tier, analysis, title), 'w') as f:
        f.write(results)

def output_analysis_time(time, N, tier, analysis):
    if not os.path.exists('{}_Results/{}'.format(tier, analysis)):
        os.makedirs('{}_Results/{}'.format(tier, analysis))
    if not os.path.exists('{}_Results/{}/{}_TIME'.format(tier, analysis, analysis)):
        with open('{}_Results/{}/{}_TIME'.format(tier, analysis, analysis), 'w') as f:
            f.write("Documents,Time")
    with open('{}_Results/{}/{}_TIME'.format(tier, analysis, analysis), 'a') as f:
        f.write("\n{},{}".format(N, time))



if __name__=='__main__':
    if len(sys.argv) != 6:
        print("Call program with desired model, data set size, number of folds in cross validation, classification tier, and type of dimensionality reduction")
        print("Possible models include:\n\tNB\n\tSVM\n\tTREE\n\tMLP\n\tALL (for all above)")
        exit()
    else:
        MODELS = sys.argv[1]
        SIZE = int(sys.argv[2])
        FOLDS = int(sys.argv[3])
        TIER = sys.argv[4]
        ANALYSIS = sys.argv[5]
    if MODELS == 'ALL':
        MODELS = ['NB', 'SVM', 'TREE', 'MLP', 'LOGREG']
    else:
        MODELS = [MODELS]

    if TIER == 'CLASS':
        SECTIONS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Y']
    elif TIER == 'SUBCLASS':
        SECTIONS = ['01','21','22','23','24','41','42','43','44','45','46','47','61','62','63']
    else:
        raise ValueError('Invalid classification tier')

    if TIER == 'CLASS':
        if os.path.exists('Class_Pickles/{}/{}'.format(ANALYSIS, SIZE)):
            print("Unpickling old data...")
            with open('Class_Pickles/{}/{}'.format(ANALYSIS, SIZE), 'r') as unpickler:
                folds = pickle.load(unpickler)
        else:
            print("Generating data...")
            x, y = generate_data_set(SIZE, TIER)
            pca_start = time.clock()
            folds = cross_validation_sets(x, y, ANALYSIS, FOLDS)
            pca_end = time.clock()
            pca_time = (pca_end-pca_start)/5.0
            #print("Writing PCA timing...")
            #output_analysis_time(pca_time, SIZE, TIER, ANALYSIS)
            #with open('Class_Pickles/{}/{}'.format(ANALYSIS, SIZE), 'w') as pickler:
            #    pickle.dump(folds, pickler)

    elif TIER == 'SUBCLASS':
        if os.path.exists('Subclass_Pickles/{}/{}'.format(ANALYSIS, SIZE)):
            print("Unpickling old data...")
            with open('Subclass_Pickles/{}/{}'.format(ANALYSIS, SIZE), 'r') as unpickler:
                folds = pickle.load(unpickler)
        else:
            print("Generating data...")
            x, y = generate_data_set(SIZE, TIER)
            pca_start = time.clock()
            folds = cross_validation_sets(x, y, FOLDS)
            pca_end = time.clock()
            pca_time = (pca_end-pca_start)/5.0
            #print("Writing PCA timing...")
            #output_analysis_time(pca_time, SIZE, TIER)
            #with open('Subclass_Pickles/{}/{}'.format(ANALYSIS, SIZE), 'w') as pickler:
            #    pickle.dump(folds, pickler)



    for MODEL in MODELS:
        start = time.clock()
        RESULTS = ""
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("----------{} model, {} documents, {} folds----------".format(MODEL, SIZE, FOLDS))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        hls = []
        mic_precs = []
        mic_recs = []
        mic_fs = []
        mac_precs = []
        mac_recs = []
        mac_fs = []
        sec_precs = []
        sec_recs = []
        sec_fs = []
        for i, fold in enumerate(folds):
            print("Processing fold {}....".format(i+1))
            x_train = fold[0][0]
            y_train = fold[0][1]
            x_test = fold[1][0]
            y_test = fold[1][1]
            clf = train_model(x_train, y_train, MODEL)

            predictions = clf.predict(x_test)

            hls.append(calculate_hamming_loss(predictions, y_test))

            mic_prec, mic_rec, mic_f, mac_prec, mac_rec, mac_f, precs, recs, fs = precision_recall(predictions, y_test)
            mic_precs.append(mic_prec)
            mic_recs.append(mic_rec)
            mic_fs.append(mic_f)
            mac_precs.append(mac_prec)
            mac_recs.append(mac_rec)
            mac_fs.append(mac_f)
            sec_precs.append(precs)
            sec_recs.append(recs)
            sec_fs.append(fs)

            print("Hamming loss: {}".format(hls[i]))
            print("Micro average:")
            print("\tprecision: {}".format(mic_prec))
            print("\trecall: {}".format(mic_rec))
            print("\tf-measure: {}".format(mic_f))

            print("Macro average:")
            print("\tprecision: {}".format(mac_prec))
            print("\trecall: {}".format(mac_rec))
            print("\tf-measure: {}".format(mac_f))

            RESULTS += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            RESULTS += "Fold number: {}\n".format(1 + i)
            RESULTS += "Hamming loss: {}\n".format(hls[i])
            RESULTS += "Micro average:\n"
            RESULTS += "\tprecision: {}".format(mic_prec)
            RESULTS += "\trecall: {}".format(mic_rec)
            RESULTS += "\tf-measure: {}\n".format(mic_f)
            RESULTS += "Macro average:\n"
            RESULTS += "\tprecision: {}".format(mac_prec)
            RESULTS += "\trecall: {}".format(mac_rec)
            RESULTS += "\tf-measure: {}\n\n".format(mac_f)

            for SECTION, prec, rec, f in zip(SECTIONS, precs, recs, fs):
                print("\t{} precision: {}\trecall: {}\tF-measure: {}".format(SECTION, prec, rec, f))
                RESULTS += "\t{} precision: {}\trecall: {}\tF-measure: {}\n".format(SECTION, prec, rec, f)
            print
            RESULTS += "\n"

        PERFORMANCE = "----------MODEL PERFORMANCE----------\nHamming loss: {}\nMicro average:\n\tPrecision: {}\n\tRecall: {}\n\tF-Measure: {}\nMacro average:\n\tPrecision: {}\n\tRecall: {}\n\tF-measure: {}\n\n".format(numpy.mean(hls), numpy.mean(mic_precs), numpy.mean(mic_recs), numpy.mean(mic_fs), numpy.mean(mac_precs), numpy.mean(mac_recs), numpy.mean(mac_fs))

        for i, SECTION in enumerate(SECTIONS):
            prec = numpy.mean([fold[i] for fold in sec_precs])
            rec = numpy.mean([fold[i] for fold in sec_recs])
            f = numpy.mean([fold[i] for fold in sec_fs])
            PERFORMANCE += "\tSection {} precision: {}\trecall: {}\tf-measure: {}\n".format(SECTION, prec, rec, f)
        print(PERFORMANCE)

        end = time.clock()
        perf_time = end-start
        RESULTS = "Performance time: {}\n\n".format(perf_time) + PERFORMANCE + '\n' + RESULTS
        output_results(RESULTS, MODEL, SIZE, TIER, ANALYSIS)

        

