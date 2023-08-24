import React from 'react';

function InputField({ label, type, name, value, onChange }) {
    return (
        <div className="mb-3">
            <label className="form-label">{label}</label>
            <input
                type={type}
                className="form-control"
                name={name}
                value={value}
                onChange={onChange}
                required={true}
            />
        </div>
    );
}


export default InputField;
