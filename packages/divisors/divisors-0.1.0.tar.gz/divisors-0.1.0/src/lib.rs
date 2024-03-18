use pyo3::prelude::*;
use ::divisors::get_divisors;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn get_divs(n: u128) -> Vec<u128> {
    get_divisors(n)
}

/// A Python module implemented in Rust.
#[pymodule]
fn divisors(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_divs, m)?)?;
    Ok(())
}
