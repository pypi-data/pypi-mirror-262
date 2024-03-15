#![deny(clippy::pedantic)]
#![deny(clippy::unwrap_used)]
#![deny(clippy::expect_used)]
#![deny(clippy::indexing_slicing)]
#![deny(clippy::panic)]
#![deny(clippy::todo)]
#![deny(clippy::unimplemented)]
#![deny(clippy::unreachable)]
#![allow(clippy::missing_errors_doc)]
#![cfg_attr(not(test), no_main)]

#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct ReinterpretCodec {
    encode_dtype: codecs_core::BufferTy,
    decode_dtype: codecs_core::BufferTy,
}

impl codecs_core::Codec for ReinterpretCodec {
    type DecodedBuffer = codecs_core::VecBuffer;
    type EncodedBuffer = codecs_core::VecBuffer;

    const CODEC_ID: &'static str = "reinterpret";

    fn from_config<'de, D: serde::Deserializer<'de>>(config: D) -> Result<Self, D::Error> {
        let codec: Self = serde::Deserialize::deserialize(config)?;

        #[allow(clippy::match_same_arms)]
        match (codec.decode_dtype, codec.encode_dtype) {
            // performing no conversion always works
            (ty_a, ty_b) if ty_a == ty_b => (),
            // converting to bytes always works
            (_, codecs_core::BufferTy::U8) => (),
            // converting from signed / floating to same-size binary always works
            (codecs_core::BufferTy::I16, codecs_core::BufferTy::U16)
            | (
                codecs_core::BufferTy::I32 | codecs_core::BufferTy::F32,
                codecs_core::BufferTy::U32,
            )
            | (
                codecs_core::BufferTy::I64 | codecs_core::BufferTy::F64,
                codecs_core::BufferTy::U64,
            ) => (),
            _ => {
                return Err(serde::de::Error::custom(format!(
                    "reinterpreting {} as {} is not allowed",
                    codec.decode_dtype, codec.encode_dtype,
                )))
            },
        };

        Ok(codec)
    }

    fn encode(
        &self,
        buf: codecs_core::BufferSlice,
        shape: &[usize],
    ) -> Result<codecs_core::ShapedBuffer<Self::EncodedBuffer>, String> {
        if buf.ty() != self.decode_dtype {
            return Err(format!(
                "Reinterpret::encode buffer dtype `{}` does not match the configured decode_dtype \
                 `{}`",
                buf.ty(),
                self.decode_dtype
            ));
        }

        let (encoded, shape) = match (&buf, self.encode_dtype) {
            (buf, ty) if buf.ty() == ty => (*buf, Vec::from(shape)),
            (buf, codecs_core::BufferTy::U8) => {
                let mut shape = Vec::from(shape);
                if let Some(last) = shape.last_mut() {
                    *last *= buf.ty().layout().size();
                }
                (codecs_core::BufferSlice::U8(buf.as_bytes()), shape)
            },
            (codecs_core::BufferSlice::I16(v), codecs_core::BufferTy::U16) => (
                codecs_core::BufferSlice::U16(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::I32(v), codecs_core::BufferTy::U32) => (
                codecs_core::BufferSlice::U32(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::F32(v), codecs_core::BufferTy::U32) => (
                codecs_core::BufferSlice::U32(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::I64(v), codecs_core::BufferTy::U64) => (
                codecs_core::BufferSlice::U64(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::F64(v), codecs_core::BufferTy::U64) => (
                codecs_core::BufferSlice::U64(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (buf, ty) => {
                return Err(format!(
                    "Reinterpret::encode reinterpreting buffer dtype `{}` as `{ty}` is not allowed",
                    buf.ty(),
                ));
            },
        };

        Ok(codecs_core::ShapedBuffer {
            shape,
            buffer: encoded.to_vec(),
        })
    }

    fn decode(
        &self,
        buf: codecs_core::BufferSlice,
        shape: &[usize],
    ) -> Result<codecs_core::ShapedBuffer<Self::DecodedBuffer>, String> {
        if buf.ty() != self.encode_dtype {
            return Err(format!(
                "Reinterpret::decode buffer dtype `{}` does not match the configured encode_dtype \
                 `{}`",
                buf.ty(),
                self.encode_dtype
            ));
        }

        let (decoded, shape) = match (&buf, self.decode_dtype) {
            (buf, ty) if buf.ty() == ty => (*buf, Vec::from(shape)),
            (codecs_core::BufferSlice::U8(v), ty) => {
                let mut shape = Vec::from(shape);
                if let Some(last) = shape.last_mut() {
                    if *last % ty.layout().size() != 0 {
                        return Err(format!(
                            "Reinterpret::decode byte buffer with shape {shape:?} cannot be \
                             reinterpreted as {ty}"
                        ));
                    }

                    *last /= ty.layout().size();
                }
                (
                    unsafe {
                        codecs_core::BufferSlice::from_data_ty_len(
                            v.as_ptr(),
                            ty,
                            v.len() / ty.layout().size(),
                        )
                    },
                    shape,
                )
            },
            (codecs_core::BufferSlice::U16(v), codecs_core::BufferTy::I16) => (
                codecs_core::BufferSlice::I16(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::U32(v), codecs_core::BufferTy::I32) => (
                codecs_core::BufferSlice::I32(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::U32(v), codecs_core::BufferTy::F32) => (
                codecs_core::BufferSlice::F32(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::U64(v), codecs_core::BufferTy::I64) => (
                codecs_core::BufferSlice::I64(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (codecs_core::BufferSlice::U64(v), codecs_core::BufferTy::F64) => (
                codecs_core::BufferSlice::F64(unsafe {
                    std::slice::from_raw_parts(v.as_ptr().cast(), v.len())
                }),
                Vec::from(shape),
            ),
            (buf, ty) => {
                return Err(format!(
                    "Reinterpret::decode reinterpreting buffer dtype `{}` as `{ty}` is not allowed",
                    buf.ty(),
                ));
            },
        };

        Ok(codecs_core::ShapedBuffer {
            shape,
            buffer: decoded.to_vec(),
        })
    }

    fn get_config<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serde::Serialize::serialize(&self, serializer)
    }
}

codecs_core_wasm::export_codec! {
    /// Codec to reinterpret data between different compatible types.
    /// Note that no conversion happens, only the meaning of the bits changes.
    ///
    /// Args:
    ///     encode_dtype (dtype): Data type to use for encoded data.
    ///     decode_dtype (dtype): Data type to use for decoded data.
    ReinterpretCodec(encode_dtype, decode_dtype)
}
