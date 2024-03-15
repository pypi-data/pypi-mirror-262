from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, PowerTransformer, RobustScaler, PolynomialFeatures
import pandas as pd
import numpy as np
import tensorflow as tf
#import matplotlib
#matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import CategoricalCrossentropy, MeanAbsoluteError, Hinge, MeanSquaredError
from tensorflow import keras
from itertools import combinations
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import os
import glob
from pandas import read_csv
from datetime import datetime
from threading import Thread
from queue import Queue

def save_log(output_dir, basename, execution_time, activity, columns_to_remove,
             logarithmic, plot_label, transformX, transformY, scalerX, scalerY,
             X_test, X_train, r2_test, mae_test, r2_train, mae_train,
             model_output_path, output_plot_file_path, output_loss_plot_path,
             epochs, optimizer, X_features, csv, dense_units, learning_rate):

    log_output_path = os.path.join(output_dir, f'{basename}_tensor.log')
    
    with open(log_output_path, 'w') as log_file:  
        model_creation_code = (
            "model = Sequential([\n"
            f"    keras.layers.Input(shape=({X_train.shape[1]},)),\n"
        )
        model_creation_code += "".join([f"    Dense({units}, activation='relu'),\n" for units in dense_units])
        model_creation_code += "    Dense(1)\n])\n"
    
    with open(log_output_path, 'w') as log_file:
        log_file.write(f'Execution Time: {execution_time}\n')
        log_file.write(f'File data input: {csv}\n')
        log_file.write(f'Activity columns(activity): {activity}\n')
        log_file.write(f'Non Feature Columns (columns_to_remove): {columns_to_remove}\n')
        log_file.write(f'Activity Log (logarithmic): {logarithmic}\n')
        log_file.write(f'Activity label in plot: {plot_label}\n')
        log_file.write(f'Transform X: {transformX}\n')
        log_file.write(f'Transform Y: {transformY}\n')
        log_file.write(f'scalerX: {scalerX}\n')
        log_file.write(f'scalerY: {scalerY}\n')
        log_file.write(f'Validation Data: {len(X_test)} molecules\n')
        log_file.write(f'Train Data: {len(X_train)} molecules\n')
        log_file.write(f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}\n')
        log_file.write(f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}\n')
        log_file.write(f'Model saved to {model_output_path}\n')
        log_file.write(f'Plot saved to {output_plot_file_path}\n')
        log_file.write(f'Loss plot saved to {output_loss_plot_path}\n')
        log_file.write("Model Creation Code:\n")
        log_file.write(model_creation_code)
        log_file.write(f'Epochs: {epochs}\n')
        log_file.write(f'optimizer: {optimizer}\n')
        log_file.write(f'Features:\n')
        log_file.write(f', '.join(X_features))

def generate_tensor_model(result_text, job_directory, csv, columns_to_remove, transformX, scalerX, all_features, activity, logarithmic, transformY, scalerY, plot_label, epochs, batch_size, dense_units, dense_activations, optimizer, learning_rate, loss_function, patience):
        def plot_function():
            # Show the plots
            queue = Queue()
            queue.get()
            queue.put("plot_ready")
        
        def plot_thread():
            # Create a new thread to run the subprocess
            thread = Thread(target=plot_function)                      
            thread.start()
            plt.show()
            
        try:
            execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            epochs = int(epochs)
            batch_size = int(batch_size)
            patience = int(patience)
            learning_rate = float(learning_rate)
            df = read_csv(csv)
            df = df.dropna()
            
            basename_with_extension = os.path.basename(csv)
            basename = os.path.splitext(basename_with_extension)[0]

            if df.empty:
                print("Error: No data points remaining after dropping NaN values.")
            else:
                # Convert IC50 to pIC50
                if logarithmic:
                    actplot = f'p{plot_label}'
                    act = f'p{plot_label}'
                    #df[activity] = pd.to_numeric(df['activity'])
                    df[act] = -np.log10(df[activity] * 1e-9)
                else:
                    actplot = plot_label
                    act = activity

                # Split features X and target Y
                columns_to_remove = [col.strip() for col in columns_to_remove.split(',')]
                columns_to_remove.append(act)
                X_features = df.drop(columns=columns_to_remove, axis=1)
                y = df[act]

                # Check if there are any data points remaining after dropping columns
                if X_features.empty:
                    print("Error: No data points remaining after dropping columns.")
                else:
                    # Initialize scalers
                    if scalerX == 'StandardScaler':
                        scaler_X = StandardScaler()
                    elif scalerX == 'RobustScaler':
                        scaler_X = RobustScaler()
                    elif scalerX == 'MinMaxScaler':
                        scaler_X = MinMaxScaler()
                    elif scalerX == 'Normalizer':
                        scaler_X = Normalizer()

                    # Initialize scalers
                    if scalerY == 'StandardScaler':
                        scaler_y = StandardScaler()
                    elif scalerY == 'RobustScaler':
                        scaler_y = RobustScaler()
                    elif scalerY == 'MinMaxScaler':
                        scaler_y = MinMaxScaler()
                    elif scalerY == 'Normalizer':
                        scaler_y = Normalizer()

                    # Transform data
                    if transformY:
                        y_normalized = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()
                    else:
                        y_normalized = y

                    if transformX:
                        X_normalized = scaler_X.fit_transform(X_features)
                    else:
                        X_normalized = X_features

                    # Split the data into training and testing sets
                    if all_features:
                        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_normalized, test_size=0.2, random_state=1)
                    else:
                        feature_list = X_features.columns
                        feature_indices = [X_features.columns.get_loc(feature) for feature in feature_list]
                        X_train, X_test, y_train, y_test = train_test_split(X_normalized[:, feature_indices], y_normalized, test_size=0.2, random_state=1)

                    # Create and compile the model
                    model = Sequential([
                        Dense(units, activation=activation) for units, activation in zip(dense_units[:-1], dense_activations[:-1])
                    ] + [Dense(dense_units[-1], activation=dense_activations[-1])])
                    
                    if optimizer == "Adam":
                        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
                    elif optimizer == "SGD":
                        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
                    elif optimizer == "RMSprop":
                        optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
                    elif optimizer == "Adagrad":
                        optimizer = tf.keras.optimizers.Adagrad(learning_rate=learning_rate)                        
                    elif optimizer == "Adadelta":
                        optimizer = tf.keras.optimizers.Adadelta(learning_rate=learning_rate)
                    
                    if loss_function == "MAE":
                        loss_function = MeanAbsoluteError() 
                        metrics = "val_loss"
                    elif loss_function == "MSE":
                        #loss_function = MeanSquaredError()
                        #metrics = "val_loss"
                        loss_function = MeanAbsoluteError() 
                        metrics = "val_loss"
                    elif loss_function == "Cross-entropy":
                        #loss_function = CategoricalCrossentropy() 
                        #metrics = "accuracy"                        
                        loss_function = MeanAbsoluteError() 
                        metrics = "val_loss"
                    elif loss_function == "Hinge":                    
                        #loss_function = Hinge() 
                        #metrics = "accuracy"
                        loss_function = MeanAbsoluteError() 
                        metrics = "val_loss"
                        
                        
                    model.compile(optimizer=optimizer, loss=loss_function)

                    # Training with early stopping
                    callback = EarlyStopping(monitor=metrics, patience=patience, verbose=1)
                    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[callback])

                    # Predict on the test data
                    y_test_pred = model.predict(X_test)
                    y_train_pred = model.predict(X_train)

                    # Convert the normalized predictions back to the original scale
                    if transformY:
                        y_test_pred_original_scale = scaler_y.inverse_transform(y_test_pred.reshape(-1, 1)).flatten()
                        y_train_pred_original_scale = scaler_y.inverse_transform(y_train_pred.reshape(-1, 1)).flatten()
                        y_test_original_scale = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()
                        y_train_original_scale = scaler_y.inverse_transform(y_train.reshape(-1, 1)).flatten()
                    else:
                        y_test_pred_original_scale = y_test_pred.flatten()
                        y_train_pred_original_scale = y_train_pred.flatten()
                        y_test_original_scale = y_test
                        y_train_original_scale = y_train

                    # Plot y vs. y_calculate
                    plt.figure(figsize=(9, 9))
                    plt.scatter(y_test_original_scale, y_test_pred_original_scale, alpha=0.5, label=f'Validation Data: {len(X_test)} molecules')
                    plt.scatter(y_train_original_scale, y_train_pred_original_scale, alpha=0.5, label=f'Train Data: {len(X_train)} molecules')

                    # Add labels to the axes
                    plt.xlabel(f'True {actplot}')
                    plt.ylabel(f'Predicted {actplot}')

                    # Set consistent axis limits
                    Ytest = y_test_original_scale
                    Ytrain = y_train_original_scale
                    lim_down = min(np.min(Ytest), np.min(Ytrain)) - 0.2 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
                    lim_up = max(np.max(Ytest), np.max(Ytrain)) + 0.2 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
                    plt.xlim(lim_down, lim_up)
                    plt.ylim(lim_down, lim_up)

                    # Add regression lines
                    z_test = np.polyfit(y_test_original_scale, y_test_pred_original_scale, 1)
                    p_test = np.poly1d(z_test)
                    z_train = np.polyfit(y_train_original_scale, y_train_pred_original_scale, 1)
                    p_train = np.poly1d(z_train)

                    # Calculate R-squared
                    r2_test = r2_score(y_test_original_scale, y_test_pred_original_scale)
                    r2_train = r2_score(y_train_original_scale, y_train_pred_original_scale)

                    # Calculate MAE
                    mae_test = mean_absolute_error(y_test_original_scale, y_test_pred_original_scale)
                    mae_train = mean_absolute_error(y_train_original_scale, y_train_pred_original_scale)

                    # Plot regression lines
                    plt.plot(y_test_original_scale, p_test(y_test_original_scale), 'b--', label=f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}')
                    plt.plot(y_train_original_scale, p_train(y_train_original_scale), 'r--', label=f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}')

                    # Add legend
                    plt.legend()

                    # Show the plot
                    print(f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}')
                    print(f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}')

                    # Menyimpan plot ke file
                    plot_filename = f'{basename}.png'
                    output_plot_file_path = os.path.join(job_directory, plot_filename)
                    plt.savefig(output_plot_file_path)
                    print(f'Plot disimpan sebagai {plot_filename}')

                    # Membuat plot kedua (train vs val loss)
                    plt.figure(figsize=(9, 6))
                    plt.plot(history.history['loss'], label='Train Loss')
                    plt.plot(history.history['val_loss'], label='Validation Loss')
                    plt.xlabel('Epochs')
                    plt.ylabel('Loss')

                    # Add legend
                    plt.legend()

                    # Menyimpan plot kedua ke file
                    loss_plot_filename = f'{basename}_loss.png'
                    output_loss_plot_path = os.path.join(job_directory, loss_plot_filename)
                    plt.savefig(output_loss_plot_path)
                    print(f'Loss plot disimpan sebagai {loss_plot_filename}')

                    # Save the model to a file
                    model_filename = f'{basename}.keras'
                    model_output_path = os.path.join(job_directory, model_filename)
                    model.save(model_output_path)

                    print(f'Model saved to {model_filename}')

                    # Simpan konfigurasi dan X_features ke file log tertentu
                    save_log(job_directory, basename, execution_time, activity, columns_to_remove,
                             logarithmic, plot_label, transformX, transformY, scalerX, scalerY,
                             X_test, X_train, r2_test, mae_test, r2_train, mae_train,
                             model_output_path, output_plot_file_path, output_loss_plot_path,
                             epochs, optimizer, X_features, csv, dense_units, learning_rate)

                    plot_thread()

        except Exception as e:
            print(f"Error: {e}")
