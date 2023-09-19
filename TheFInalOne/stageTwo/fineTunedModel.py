from transformers import RobertaTokenizerFast, RobertaForMaskedLM, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Step 1: Load the tokenizer
tokenizer = RobertaTokenizerFast.from_pretrained("deepset/tinyroberta-squad2")

# Step 2: Create a dataset from your text file
dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path="Barack_Obama.txt",  # path to your file
    block_size=128,
)

# Step 3: Create a data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15,
)

# Step 4: Load the model
model = RobertaForMaskedLM.from_pretrained("deepset/tinyroberta-squad2")

# Step 5: Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=64,
    save_steps=10_000,
    save_total_limit=2,
)

# Step 6: Create the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Step 7: Train the model
trainer.train()

# Step 8: Save the model
model.save_pretrained("./fine_tuned_model")
