use pyo3::prelude::*;
use orion::aead;

const XXX: &str = "aa.aa+d0sd1411a0sd1411a$sd14@1a0";

#[pyfunction]
pub fn xx1xx2(s: String) -> Vec<u8> {
  let secret_key = aead::SecretKey::from_slice(XXX.as_bytes()).unwrap();
  let ciphertext = aead::seal(&secret_key, s.as_bytes()).unwrap();
  ciphertext.into()
}

#[pyfunction]
pub fn xx2xx1(b: Vec<u8>) -> Vec<u8> {
  let secret_key = aead::SecretKey::from_slice(XXX.as_bytes()).unwrap();
  let buf: Vec<u8> = b.into();
  let decrypted_data = aead::open(&secret_key, &buf);
  decrypted_data.unwrap().into()
}


/// A Python module implemented in Rust.
#[pymodule]
fn mlencrypt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(xx1xx2, m)?)?;
    m.add_function(wrap_pyfunction!(xx2xx1, m)?)?;
    Ok(())
}
