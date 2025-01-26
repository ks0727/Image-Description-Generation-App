import torch
from torch.utils.data import DataLoader
import argparse
from transformers import AdamW
from transformers import BlipProcessor, BlipForConditionalGeneration
from datasets import load_dataset

def main(args):
    model = BlipForConditionalGeneration.from_pretrained(args.model_path)
    processor = BlipProcessor.from_pretrained(args.model_path)
    
    dataset = load_dataset('json', data_files='dataset.json', split='train')
    train_dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    
    optimizer = AdamW(model.parameters(), lr=args.lr)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for epoch in range(args.epoch_num):
        model.train()
        epoch_loss = 0.0

        for batch in train_dataloader:
            pixel_values = batch["pixel_values"].to("cuda" if torch.cuda.is_available() else "cpu")
            captions = batch["caption"]
            
            inputs = processor(
                images=pixel_values,
                text=captions, 
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(device=device)

            outputs = model(*inputs)
            
            optimizer.zero_grad()
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        print(f"Epoch {epoch+1} loss: {epoch_loss / len(train_dataloader)}")

    model.save_pretrained("./checkpoints")
    processor.save_pretrained("./checkpoints")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',type=str,default="Salesforce/blip-image-captioning-base",
                        help="path to the model you want to train")
    parser.add_argument('--lr',type=float,default=2e-5,
                        help="learning rate")
    parser.add_argument('--batch_size',type=int,default=8,
                        help="batch size of training")
    parser.add_argument('--epoch_num',type=int,default=3,
                        help="number of epoch of training")
    parser.add_argument('--save_path',type=str,default="../checkpoints",
                        help="path to save your model")
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)

