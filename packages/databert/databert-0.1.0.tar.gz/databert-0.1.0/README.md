# DataBERT Classifier for Dataset Identification

This package provides a comprehensive toolset for training and deploying BERT-based classifiers for text classification tasks, ranging from binary to multiclass problems. Leveraging the power of the `transformers` library, it simplifies the process of fine-tuning pre-trained BERT models and offers functionalities to evaluate, save, and deploy these models effectively.

## Features

- Easy-to-use classes for training and using BERT models for text classification.
- Preprocessing and tokenization tailored for BERT's requirements.
- Calculation of various evaluation metrics including accuracy, precision, recall, specificity, and ROC-AUC.
- Functionality to save and load trained models and tokenizers.
- Capability to push trained models to the Hugging Face Hub.

## Installation

To use this package, you need to install the required libraries. It's recommended to use a virtual environment:

```bash
pip install transformers torch sklearn numpy
```

## Usage

### Training DataBERT

1. **Initialize the Classifier**

You can initialize the `TrainBERTClassifier` with desired training parameters. Here's an example:

```python
from bert_classifier import TrainBERTClassifier

classifier = TrainBERTClassifier(
    model_name='bert-base-uncased',
    num_labels=2,
    max_length=128,
    batch_size=32,
    learning_rate=2e-5,
    epochs=3
)
```

2. **Prepare your data**

Organize your text data and labels for training and validation. For example:

```python
train_texts = ['This is the first text', 'Here is another one']
train_labels = [0, 1]

val_texts = ['This text is for validation', 'Another validation text']
val_labels = [0, 1]
```

3. **Train the model**

Use the `train` method to fine-tune the BERT model on your data:

```python
classifier.train(train_texts, train_labels, val_texts, val_labels)
```

4. **Evaluate the Model**
:
After training, the model's performance metrics for the validation set will be printed automatically, including accuracy, precision, recall, specificity, and ROC-AUC.

5. **Save the Model**:

Save your trained model and tokenizer for later use:

```python
classifier.save_model_and_tokenizer('path/to/save/directory')
```

# Using the Trained BERT Classifier

After training and saving your model, you can use it for classifying new texts:

1. **Initialize the Classifier with the Trained Model**:

Load your trained model and tokenizer:

```python
from bert_classifier import BERTClassifier

model_path = 'path/to/save/directory/model'
tokenizer_name = 'bert-base-uncased'  # Or path to tokenizer if you saved it

bert_classifier = BERTClassifier(model_path, tokenizer_name)
```

2. **Classify new texts**

You can now use the classifier to predict the class of new texts:

```python
text = "Example text to classify"
prediction, confidence = bert_classifier.predict(text)
print(f"Predicted class: {prediction} with confidence {confidence}")
```

# Contributions

Contributions to this package are welcome. Please follow conventional commit messages and ensure code quality for any pull requests.

# License

This project is licensed under the MIT License - see the LICENSE file for details.




