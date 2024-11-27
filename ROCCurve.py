import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def plot_roc_curve(ground_truth, technique_scores):
    """Plot the ROC curve for multiple techniques."""
    plt.figure(figsize=(10, 8))

    for technique, scores in technique_scores.items():
        fpr, tpr, _ = roc_curve(ground_truth, scores)
        roc_auc = auc(fpr, tpr)

        # plots the curve with a line for random chance as well
        plt.plot(fpr, tpr, label=f'{technique} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')  
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve for Hallucination Detection Techniques')
    plt.legend(loc='lower right')
    plt.show()

def main():
    # ground truth data
    ground_truth_sac3 = [
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
        0, 1, 1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]
    ground_truth_cove = [
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
        1, 0, 1, 1, 1, 1, 1, 1, 1, 1
    ]
    
    technique_scores_sac3 = {
        "sac3": [
            0.83, 0.87, 0.9, 0.92, 0.97, 0.92, 0.93, 0.92, 0.9, 0.9,
            0.93, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
            0.85, 0.87, 0.92, 0.8, 0.95, 0.9, 0.88, 0.9, 0.83, 0.92,
            0.92, 0.95, 0.95, 0.93, 0.9, 0.92, 0.92, 0.93, 0.95, 0.95,
            0.93, 0.9, 0.95, 0.95, 0.95, 0.95, 0.97, 0.95, 0.93, 0.93,
            0.97, 0.93, 0.93, 0.88, 0.93, 0.95, 0.88, 0.93, 0.93, 0.92,
            0.92, 0.95, 0.95, 0.92, 0.95, 0.93, 0.88, 0.92, 0.95, 0.95,
            0.93, 0.9, 0.9, 0.92, 0.92, 0.9, 0.9, 0.92, 0.9, 0.92,
            0.9, 0.92, 0.83, 0.86, 0.93, 0.88, 0.97, 0.98, 0.93, 0.86
        ]
    }
    technique_scores_cove = {
        "runCove": [
            0.9, 0.9, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 1, 0.95,
            0.85, 0.9, 0.95, 1, 0.95, 0.95, 0.95, 0.9, 0.9, 0.9,
            0.9, 0.9, 0.95, 0.9, 0.95, 0.95, 0.9, 0.9, 0.9, 0.95,
            1, 0.95, 0.95, 1, 0.95, 0.95, 0.95, 0.95, 0.95, 1,
            0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95,
            0.95, 1, 0.95, 1, 0.95, 0.95, 0.95, 0.9, 0.9, 0.95,
            0.9, 0.9, 1, 1, 0.85, 0.9, 0.95, 0.95, 1, 0.95,
            0.95, 0.95, 0.9, 1, 0.9, 0.9, 0.95, 0.95, 0.95, 0.95,
            0.9, 0.95, 0.95, 0.9, 0.95, 0.85, 1, 1, 0.95, 0.95
        ]
    }

    # takes in the two arrays 
    plot_roc_curve(ground_truth_sac3, technique_scores_sac3)

if __name__ == "__main__":
    main()
