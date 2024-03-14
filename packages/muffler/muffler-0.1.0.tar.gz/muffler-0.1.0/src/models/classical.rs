//! A model that relies on classical ML techniques to denoise time-series data.

use ndarray::prelude::*;
use rayon::prelude::*;
use smartcore::{
    api::SupervisedEstimator,
    linalg::basic::{arrays::Array2, matrix::DenseMatrix},
};

/// A model that can be trained, evaluated, and used for prediction.
///
/// # Type Parameters
///
/// * `M`: The type of the model.
/// * `P`: The type of the model parameters.
pub trait Classical<M, P>: Sized + Send + Sync
where
    M: SupervisedEstimator<DenseMatrix<f32>, Array1<f32>, P> + Send + Sync,
    P: Clone + Send + Sync,
{
    /// Creates a new model.
    fn new(models: Vec<M>, window_size: usize) -> Self;

    /// Returns the inner models.
    fn models(&self) -> &[M];

    /// Returns the window size.
    fn window_size(&self) -> usize;

    /// Trains the model.
    ///
    /// # Parameters
    ///
    /// * `samples`: The time-series samples to create the data from.
    /// * `window_size`: The number of elements in each window.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The trained model.
    fn train(
        samples: &ndarray::Array2<f32>,
        window_size: usize,
        stride: usize,
        parameters: P,
    ) -> Result<Self, String> {
        let (windows, _) = crate::data::create_windows(samples, window_size, stride);
        let inner_models = (0..window_size)
            .into_par_iter()
            .map(|i| {
                let (train_x, train_y) = crate::data::windows_to_train(&windows, i);
                let train_x = DenseMatrix::from_slice(&train_x);
                M::fit(&train_x, &train_y, parameters.clone())
                    .map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        Ok(Self::new(inner_models, window_size))
    }

    /// Predicts the denoised time-series using the model.
    ///
    /// # Parameters
    ///
    /// * `x`: The input data to predict the target data.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The denoised time-series.
    fn denoise(
        &self,
        samples: &ndarray::Array2<f32>,
        stride: usize,
    ) -> Result<ndarray::Array2<f32>, String> {
        let (windows, starts) =
            crate::data::create_windows(samples, self.window_size(), stride);
        let predicted = (0..self.window_size())
            .into_par_iter()
            .map(|i| {
                let (test_x, _) = crate::data::windows_to_train(&windows, i);
                let test_x = DenseMatrix::from_slice(&test_x);
                let model = &self.models()[i];
                M::predict(model, &test_x).map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        let predicted = predicted.iter().map(ArrayBase::view).collect::<Vec<_>>();
        let predicted =
            ndarray::stack(Axis(1), &predicted).map_err(|e| e.to_string())?;

        let out_shape = (samples.len_of(Axis(0)), samples.len_of(Axis(1)));
        Ok(crate::data::reassemble(predicted, out_shape, &starts))
    }
}
