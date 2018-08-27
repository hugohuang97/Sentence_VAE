import numpy as np
# import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
from gru_model_class import ModelStruct
import data_utils

batch_size = 128

# load data and fit it to batch size
train = data_utils.load_data('train.npz', 'index', np.int32)
valid = data_utils.load_data('valid.npz', 'index', np.int32)
test = data_utils.load_data('test.npz', 'index', np.int32)
train = data_utils.fit_batch(train, batch_size)
valid = data_utils.fit_batch(valid, batch_size)
test = data_utils.fit_batch(test, batch_size)

# define model hyper-parameters
seq_len = train.shape[1]
embedding_matrix = data_utils.load_data('trimmed_glove.npz', 'embeddings', np.float32)
latent_size = 64
batch_shape = (batch_size, seq_len)
plot = False

# construct models
model_struct = ModelStruct(batch_shape, embedding_matrix, latent_size)
# vae = model_struct.assemble_vae_train()
encoder = model_struct.assemble_encoder_infer()
decoder = model_struct.assemble_decoder_infer()

if plot:
    plot_model(vae, to_file='vae.png', show_shapes=True, show_layer_names=True)
    plot_model(encoder, to_file='encoder.png', show_shapes=True, show_layer_names=True)
    plot_model(decoder, to_file='decoder.png', show_shapes=True, show_layer_names=True)

#####----- 2 problems: accuracy and generation -----######

# display and fit model
# vae.summary()
# encoder.summary()
# decoder.summary()
# vae.fit(train, train, batch_size=batch_size, epochs=1, shuffle=True, validation_data=(valid, valid))

# loss, acc = vae.evaluate(test, test, batch_size=batch_size)
# print('evaluation result')
# print('loss =', loss, 'accuracy =', acc)

# reconstructed = vae.predict(test[:batch_size], batch_size=batch_size)
# predicted = np.argmax(reconstructed, axis=-1)
# print('shape of predicted:', predicted.shape)
# print(predicted)
# print('test.shape', test.shape)
state = encoder.predict(test[0].reshape(1, -1))
out = np.array(1).reshape(1, -1)  # initial "start" token
# predicted = []
# for _ in range(seq_len):
out, state = decoder.predict([out, state])
print('out.shape', out.shape)
print('state.shape', state.shape)
out = np.argmax(out, axis=-1)
print('after argmax, out.shape', out.shape)

#     predicted.append(out.reshape(-1,))
# predicted = np.array(predicted)
# print('test[0]')
# print(test[0])
# print('predicted')
# print(predicted)

# fig = plt.figure()
# ax1 = fig.add_subplot(1, 2, 1)
# ax1.imshow(x_test[0], cmap='gray')
# ax1.set_axis_off()
#
# ax2 = fig.add_subplot(1, 2, 2)
# ax2.imshow(predicted, cmap='gray')
# ax2.set_axis_off()
#
# plt.show()

# show results
# n = 5

# encoded_means, _ = encoder.predict(test_imgs)
# decoded_imgs_means = decoder.predict(encoded_means).reshape(-1, 28, 28)
# decoded_imgs_noise = vae.predict(test_imgs).reshape(-1, 28, 28)
# test_imgs = x_test[0: n]
# recon_imgs = reconstructed[0: n]
# fig = plt.figure()
# for i in range(1, n + 1):
#     # display original
#     ax = fig.add_subplot(2, n, i)
#     ax.imshow(test_imgs[i - 1], cmap='gray')
#     ax.set_axis_off()
#
#     # display mean reconstruction
#     ax = fig.add_subplot(2, n, i + n)
#     ax.imshow(recon_imgs[i - 1], cmap='gray')
#     ax.set_axis_off()
#
#     # display noisy reconstruction
#     # ax = fig.add_subplot(3, n, i + 2 * n)
#     # plt.imshow(decoded_imgs_noise[i - 1], cmap='gray')
#     # ax.set_axis_off()
#
# plt.show()
