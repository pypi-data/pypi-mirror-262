use super::py_network::PyNetwork;
use bitcoin::util::address::Address;
use bitcoin::util::key::PublicKey;
use pyo3::prelude::*;

#[pyclass(name = "Address")]
struct PyAddress(Address);

#[pymethods]
impl PyAddress {
    fn __str__(&self) -> String {
        format!("{}", self.0)
    }
}

#[pyclass(name = "PublicKey")]
pub struct PyPublicKey(pub PublicKey);

#[pymethods]
impl PyPublicKey {
    fn to_string(&self) -> PyResult<String> {
        Ok(self.0.to_string())
    }

    fn p2pkh_address(&self, network: PyNetwork) -> PyAddress {
        PyAddress(Address::p2pkh(&self.0, network.into()))
    }

    fn p2wpkh_address(&self, network: PyNetwork) -> PyResult<PyAddress> {
        Address::p2wpkh(&self.0, network.into())
            .map(PyAddress)
            .map_err(|err| {
                pyo3::exceptions::PyValueError::new_err(format!(
                    "Error creating p2wpkh address: {:?}",
                    err
                ))
            })
    }

    fn p2shwpkh_address(&self, network: PyNetwork) -> PyResult<PyAddress> {
        Address::p2shwpkh(&self.0, network.into())
            .map(PyAddress)
            .map_err(|err| {
                pyo3::exceptions::PyValueError::new_err(format!(
                    "Error creating p2shwpkh address: {:?}",
                    err
                ))
            })
    }
}
