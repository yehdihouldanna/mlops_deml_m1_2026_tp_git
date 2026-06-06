import math
import random


# --- Data ---

print("--------------------------------------------------------")
print("ML Pipeline: From Data to Metrics")
print("--------------------------------------------------------")

def load_data():
    """Iris dataset hardcoded as (sepal_len, sepal_w, petal_len, petal_w, label)."""
    raw = [
        (5.1,3.5,1.4,0.2,0),(4.9,3.0,1.4,0.2,0),(4.7,3.2,1.3,0.2,0),
        (4.6,3.1,1.5,0.2,0),(5.0,3.6,1.4,0.2,0),(5.4,3.9,1.7,0.4,0),
        (6.4,3.2,4.5,1.5,1),(6.9,3.1,4.9,1.5,1),(5.5,2.3,4.0,1.3,1),
        (6.5,2.8,4.6,1.5,1),(5.7,2.8,4.5,1.3,1),(6.3,3.3,4.7,1.6,1),
        (6.3,3.3,6.0,2.5,2),(5.8,2.7,5.1,1.9,2),(7.1,3.0,5.9,2.1,2),
        (6.3,2.9,5.6,1.8,2),(6.5,3.0,5.8,2.2,2),(7.6,3.0,6.6,2.1,2),
    ]
    X = [list(r[:4]) for r in raw]
    y = [r[4] for r in raw]
    print(f"Dataset: {len(X)} samples, {len(X[0])} features, {len(set(y))} classes")
    return X, y


# --- Preprocessing ---

def train_test_split(X, y, test_size=0.2, seed=42):
    random.seed(seed)
    data = list(zip(X, y))
    random.shuffle(data)
    split = int(len(data) * (1 - test_size))
    train, test = data[:split], data[split:]
    X_tr, y_tr = [d[0] for d in train], [d[1] for d in train]
    X_te, y_te = [d[0] for d in test], [d[1] for d in test]
    return X_tr, X_te, y_tr, y_te


def standardize(X_train, X_test):
    n_feat = len(X_train[0])
    means = [sum(row[j] for row in X_train) / len(X_train) for j in range(n_feat)]
    stds  = [
        math.sqrt(sum((row[j] - means[j])**2 for row in X_train) / len(X_train))
        for j in range(n_feat)
    ]
    def scale(X):
        return [
            [(row[j] - means[j]) / (stds[j] if stds[j] else 1) for j in range(n_feat)]
            for row in X
        ]
    return scale(X_train), scale(X_test)


# --- Model: k-Nearest Neighbors ---

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def knn_predict(X_train, y_train, X_test, k=3):
    preds = []
    for point in X_test:
        dists = sorted(enumerate(euclidean(point, tr) for tr in X_train), key=lambda x: x[1])
        neighbors = [y_train[i] for i, _ in dists[:k]]
        preds.append(max(set(neighbors), key=neighbors.count))
    return preds


# --- Metrics ---

def accuracy(y_true, y_pred):
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)


def report(y_true, y_pred, classes=None):
    classes = classes or sorted(set(y_true))
    print(f"\n{'Class':<8} {'Precision':<12} {'Recall':<10} {'F1'}")
    print("-" * 44)
    for c in classes:
        tp = sum(t == c and p == c for t, p in zip(y_true, y_pred))
        fp = sum(t != c and p == c for t, p in zip(y_true, y_pred))
        fn = sum(t == c and p != c for t, p in zip(y_true, y_pred))
        prec = tp / (tp + fp) if (tp + fp) else 0
        rec  = tp / (tp + fn) if (tp + fn) else 0
        f1   = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
        print(f"{c:<8} {prec:<12.2f} {rec:<10.2f} {f1:.2f}")


# --- Pipeline ---

def run():
    print("=== ML Pipeline ===\n")

    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    X_train, X_test = standardize(X_train, X_test)

    y_pred = knn_predict(X_train, y_train, X_test, k=3)

    acc = accuracy(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}")
    report(y_test, y_pred)


if __name__ == "__main__":
    run()
