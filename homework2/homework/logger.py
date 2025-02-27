import torch
import torch.utils.tensorboard as tb

def test_logging(logger: tb.SummaryWriter):
    """
    Your code here - finish logging the dummy loss and accuracy

    For training, log the training loss every iteration and the average accuracy every epoch
    Call the loss 'train_loss' and accuracy 'train_accuracy'

    For validation, log only the average accuracy every epoch
    Call the accuracy 'val_accuracy'

    Make sure the logging is in the correct spot so the global_step is set correctly,
    for epoch=0, iteration=0: global_step=0
    """
    global_step = 0
    for epoch in range(10):
        metrics = {"train_acc": [], "val_acc": []}
        epoch_train_loss = 0.0

        # example training loop
        torch.manual_seed(epoch)
        for iteration in range(20):
            dummy_train_loss = 0.9 ** (epoch + iteration / 20.0)
            dummy_train_accuracy = epoch / 10.0 + torch.randn(10)

            # log train_loss
            logger.add_scalar("train_loss", dummy_train_loss, global_step=global_step)
            epoch_train_loss += dummy_train_loss

            # save train accuracy to metrics
            metrics["train_acc"].append(dummy_train_accuracy.mean().item())
            global_step += 1

        # log average train_loss and train_accuracy
        avg_train_loss = epoch_train_loss / 20
        avg_train_accuracy = sum(metrics["train_acc"]) / len(metrics["train_acc"])
        logger.add_scalar('avg_train_loss', avg_train_loss, global_step=global_step)
        logger.add_scalar('train_accuracy', avg_train_accuracy, global_step=global_step)
        print(f"Epoch {epoch}: avg_train_loss = {avg_train_loss}, train_accuracy = {avg_train_accuracy}")

        # example validation loop
        torch.manual_seed(epoch)
        for _ in range(10):
            dummy_validation_accuracy = epoch / 10.0 + torch.randn(10)

            # save validation accuracy to metrics
            metrics["val_acc"].append(dummy_validation_accuracy.mean().item())

        # log average val_accuracy
        avg_val_accuracy = sum(metrics["val_acc"]) / len(metrics["val_acc"])
        logger.add_scalar('val_accuracy', avg_val_accuracy, global_step=global_step)
        print(f"Epoch {epoch}: val_accuracy = {avg_val_accuracy}")

if __name__ == "__main__":
    from argparse import ArgumentParser
    from datetime import datetime
    from pathlib import Path

    parser = ArgumentParser()
    parser.add_argument("--exp_dir", type=str, default="logs")
    args = parser.parse_args()

    log_dir = Path(args.exp_dir) / f"logger_{datetime.now().strftime('%m%d_%H%M%S')}"
    logger = tb.SummaryWriter(log_dir)

    test_logging(logger)