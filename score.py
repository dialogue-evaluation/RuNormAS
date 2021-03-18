# encoding=utf-8
import sys
import os

import re

generic_size = 536
named_size = 4370

def regularize(text):
    text = re.sub("Ё", "Е", text)
    text = re.sub("ё", "е", text)
    text = re.sub(" +", " ", text)

    return text

def generic_score(true_dir, set_dir):
    if len(os.listdir(set_dir)) != generic_size:
        return 0.0
    filenames = os.listdir(f"{true_dir}/generic")
    
    n = 0
    hits = 0

    for name in filenames:
        gt = open(f"{true_dir}/generic/{name}", encoding='utf-8').read().strip()

        gt = regularize(gt)

        gt_lines = gt.split('\n')

        if not os.path.exists(f"{set_dir}/{name}"):
            return 0.0

        sub = open(f"{set_dir}/{name}", encoding='utf-8').read().strip()

        sub = regularize(sub)

        sub_lines = sub.split('\n')

        for gt, sub in zip(gt_lines, sub_lines):
            n += 1
            if gt.lower() == sub.lower():
                hits += 1

    return hits / n

def named_score(true_dir, set_dir):
    if len(os.listdir(set_dir)) != named_size:
        return 0.0
    filenames = os.listdir(f"{true_dir}/named")

    n = 0
    hits = 0

    for name in filenames:
        gt = open(f"{true_dir}/named/{name}", encoding='utf-8').read().strip()

        gt = regularize(gt)

        gt_lines = gt.split('\n')

        if not os.path.exists(f"{set_dir}/{name}"):
            return 0.0

        sub = open(f"{set_dir}/{name}", encoding='utf-8').read().strip()

        sub = regularize(sub)

        sub_lines = sub.split('\n')

        for gt, sub in zip(gt_lines, sub_lines):
            n += 1
            if gt == sub:
                hits += 1

    return hits / n


if __name__ == "__main__":
    output_stream = sys.stdout

    true_dir = os.path.join(sys.argv[1], "ref")
    predict_dir = os.path.join(sys.argv[1], "res")
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    output_stream = open(os.path.join(sys.argv[2], "scores.txt"), "w")

    set_1_dir = os.path.join(predict_dir, "generic")
    set_2_dir = os.path.join(predict_dir, "named")

    set_1_score = 0.0
    set_2_score = 0.0

    # Generic spans
    if not os.path.exists(set_1_dir) or len(os.listdir(set_1_dir)) == 0:
        set_1_score = 0.0
    else:   
        set_1_score = generic_score(true_dir, set_1_dir)

    # Named entities
    if not os.path.exists(set_2_dir) or len(os.listdir(set_2_dir)) == 0:
        set_2_score = 0.0
    else:
        set_2_score = named_score(true_dir, set_2_dir)

    output_stream.write("set_1_score: %0.12f\n" % set_1_score)
    output_stream.write("set_2_score: %0.12f\n" % set_2_score)

    output_stream.close()
