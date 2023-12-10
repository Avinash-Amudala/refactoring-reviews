import matplotlib.pyplot as plt
import seaborn as sns

def generate_confusion_matrix_plot(y_true, y_pred):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10,7))
    sns.heatmap(cm, annot=True)
    plt.xlabel('ChatGPT Label')
    plt.ylabel('Model Prediction')
    plt.title('Confusion Matrix')
    plt.savefig('static/confusion_matrix.png')