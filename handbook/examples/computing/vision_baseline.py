"""Synthetic 8x8 grayscale images expose lighting shift and held-out error."""
import argparse
from pathlib import Path


def image(dark_count, background=180):
    return [60] * dark_count + [background] * (64 - dark_count)


def dark_pixels(pixels):
    return sum(value < 100 for value in pixels)


def records():
    train = [("train-A", 0, image(0)), ("train-A", 0, image(1)),
             ("train-B", 0, image(2)), ("train-A", 1, image(4)),
             ("train-B", 1, image(6)), ("train-B", 1, image(8))]
    test = [("test-C", 1, image(4)), ("test-C", 1, image(6)),
            ("test-C", 1, image(8)), ("test-C", 1, image(2)),
            ("test-C", 0, image(0)), ("test-C", 0, image(1)),
            ("test-D", 0, image(0, 80)), ("test-D", 0, image(1, 80))]
    return train, test


def choose_threshold(train):
    # Smallest equally accurate threshold; training records only.
    return min(range(66), key=lambda threshold: sum(
        (dark_pixels(pixels) >= threshold) != bool(label)
        for _, label, pixels in train))


def evaluate(rows, threshold):
    counts = dict(tp=0, fp=0, tn=0, fn=0)
    for _, label, pixels in rows:
        predicted = dark_pixels(pixels) >= threshold
        if predicted and label:
            counts["tp"] += 1
        elif predicted:
            counts["fp"] += 1
        elif label:
            counts["fn"] += 1
        else:
            counts["tn"] += 1
    tp, fp, tn, fn = [counts[key] for key in ["tp", "fp", "tn", "fn"]]
    counts.update(accuracy=(tp + tn) / len(rows) if rows else None,
                  precision=tp / (tp + fp) if tp + fp else None,
                  recall=tp / (tp + fn) if tp + fn else None)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, help="Optional folder for readable PGM fixtures")
    args = parser.parse_args()
    train, test = records()
    threshold = choose_threshold(train)
    print(f"threshold={threshold} dark pixels; training accuracy={evaluate(train, threshold)['accuracy']:.3f}")
    result = evaluate(test, threshold)
    print("held-out " + " ".join(f"{key}={result[key]}" for key in ["tp", "fp", "tn", "fn"]))
    print(" ".join(f"{key}={result[key]:.3f}" for key in ["accuracy", "precision", "recall"]))
    if args.images:
        args.images.mkdir(parents=True, exist_ok=True)
        for index, (session, label, pixels) in enumerate(test):
            path = args.images / f"{index:02d}-{session}-label{label}.pgm"
            path.write_text("P2\n8 8\n255\n" + "\n".join(
                " ".join(str(value) for value in pixels[i:i + 8]) for i in range(0, 64, 8)) + "\n")


if __name__ == "__main__":
    main()
