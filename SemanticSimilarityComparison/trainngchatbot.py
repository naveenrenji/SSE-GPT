import torch
from transformers import AutoTokenizer, TextDataset, DataCollatorForLanguageModeling, TrainingArguments, Trainer, AutoModelForCausalLM

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(dim=-1)
    return {"perplexity": torch.exp(torch.nn.CrossEntropyLoss()(logits.view(-1, logits.size(-1)), labels.view(-1))).item()}

def load_dataset(file_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128,
    )
    return train_dataset

def create_data_collator(tokenizer):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return data_collator

def setup_training(tokenizer, dataset, data_collator):
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=100,
        per_device_train_batch_size=1,
        save_steps=10_000,
        save_total_limit=2,
        learning_rate=5e-5,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
        compute_metrics=compute_metrics
    )
    return trainer

def train_model(trainer):
    trainer.train()

# setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {device}")
print(torch.cuda.get_device_name(0))



model_name = 'mosaicml/mpt-30b-chat'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# load dataset
dataset = load_dataset("Barack_Obama.txt", tokenizer)

# create data collator
data_collator = create_data_collator(tokenizer)

# setup training
trainer = setup_training(tokenizer, dataset, data_collator)

# train
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {device}")

train_model(trainer)

# save the fine-tuned model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
