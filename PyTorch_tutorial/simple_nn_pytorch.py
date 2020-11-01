import torch
N, D_in, H, D_out = 4,2, 1, 1
x = torch.tensor([
    [-2, -1],  # Alice
    [25, 6],   # Bob
    [17, 4],   # Charlie
    [-15, -6],  # Diana
], dtype=torch.float,requires_grad=True)
y = torch.tensor([
    [1],  # Alice
    [0],  # Bob
    [0],  # Charlie
    [1],  # Diana
], dtype=torch.float)

model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.Sigmoid()
)

loss_fn = torch.nn.MSELoss(reduction="mean")

learning_rate = 0.1
epochs = 1000
for epoch in range(epochs):
    y_pred = model(x)  #  feed_forward
    loss = loss_fn(y_pred, y)
    if epoch % 100 == 0:
        print("Epoch %d loss: %.3f" % (epoch, loss.item()))

    model.zero_grad()

    loss.backward()
    with torch.no_grad():
        for param in model.parameters():
            param -= learning_rate * param.grad

# Make some predictions
emily = torch.tensor([-7, -3], dtype=torch.float)  # 128 pounds, 63 inches
frank = torch.tensor([20, 2], dtype=torch.float)  # 155 pounds, 68 inches
seb = torch.tensor([30.34669663866,4.0787])
print("Emily: %.3f" % model(emily))  # 0.951 - F
print("Frank: %.3f" % model(frank))  # 0.039 - M
print("Seb: %.3f" % model(seb))
