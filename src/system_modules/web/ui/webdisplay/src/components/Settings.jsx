import { useState, useMemo, memo} from "react";

export default function SettingsPage({}) {
    const domain_prefix = "devices.device";
    const settings = useMemo(() => [
   {
        domain: "devices.device", 
        version: "V1", 
        setting_name: "On", 
        default_value: true, 
        value: null,
        value_type: "bool",
        description: "Test boolean setting", 
        validation_data: {}, 
        user_facing: true
    },
    {
        domain: "devices.device", 
        version: "V1", 
        setting_name: "Name", 
        default_value: null,
        value: null,
        value_type: "string",
        description: "Test string setting", 
        validation_data: {}, 
        user_facing: true
    }, 
    {
        domain: "devices.device.content", 
        version: "V1", 
        setting_name: "On", 
        default_value: true, 
        value_type: "bool",
        value: null,
        description: "Test boolean setting", 
        validation_data: {}, 
        user_facing: true
    }
], []);

    const [values, setValues] = useState(() =>
        Object.fromEntries(settings.map(s => [s.domain + "." + s.setting_name, s.default_value]))
    );

    const [errors, setErrors] = useState({});
    const [dirty, setDirty] = useState(false);

    function updateValue(setting, value) {
        const error = validate(setting, value);
        console.log(value);

        setValues(v => ({ ...v, [setting.domain + "." + setting.setting_name]: value }));
        setErrors(e => ({ ...e, [setting.domain + "." + setting.setting_name]: error }));
        setDirty(true);
    }

    return (
        <>
        <SettingsPanel settings={settings} domain_prefix={domain_prefix} values={values} errors={errors} updateValue={updateValue}/>
        </>
    )
}

function SettingInput({ setting, value, onChange }) {
    if (value == null) {
        value = setting.default_value;
    }
    switch (setting.value_type) {
        case "bool":
        return (
            <input
            type="checkbox"
            checked={!!value}
            onChange={e =>
                onChange(setting, e.target.checked)
            }
            className="w-5 h-5"
            />
        );

        case "string":
        return (
            <input
            type="text"
            value={value ?? ""}
            onChange={e =>
                onChange(setting, e.target.value)
            }
            className="bg-gray-700 rounded px-2 py-1"
            />
        );

        default:
        return <span className="text-red-400">Unsupported</span>;
    }
}


function buildDomainTree(settings, domain_prefix = "") {
  const root = {};
  console.log(domain_prefix)

  for (const setting of settings) {
    let setting_domain = setting.domain
    if ( !setting_domain.startsWith(domain_prefix)) {
        continue
    }
    setting_domain = setting_domain.slice(domain_prefix.lastIndexOf(".") + 1);
    const parts = setting_domain.split(".");
    console.log(parts)
    let current = root;

    for (const part of parts) {
      current.children ??= {};
      current.children[part] ??= {};
      current = current.children[part];
    }

    current.settings ??= [];
    current.settings.push(setting);
  }

  return root.children ?? {};
}

function validate(setting, value) {
  const v = setting.validation_data ?? {};

  if (setting.value_type === "string") {
    if (v.min_length && value.length < v.min_length)
      return `Must be at least ${v.min_length} characters`;

    if (v.max_length && value.length > v.max_length)
      return `Must be at most ${v.max_length} characters`;

    if (v.regex && !new RegExp(v.regex).test(value))
      return "Invalid format";
  }

  return null;
}

function toTitleCase(data) {
    let words = data.split("_")
    for (let i=0; i<words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1).toLowerCase()
    };
    return words.join(" ")
}

function SettingsPanel({ settings, domain_prefix, values, errors, updateValue}) {
    const tree = useMemo(() => buildDomainTree(settings, domain_prefix));

    return (
        <div className="space-y-6">
        {Object.entries(tree).map(([key, node]) => (
            <DomainNode key={key} name={toTitleCase(key)} node={node} depth={0} values={values} errors={errors} updateValue={updateValue}/>
        ))}
        </div>
    );
}

function DomainNode({ name, node, depth , values, errors, updateValue}) {
    return (
        <section className="bg-gray-900 rounded p-4">
        <h2
            className="font-semibold mb-3"
            style={{ marginLeft: (depth + 1) * 12 }}
        >
            {name}
        </h2>
        <hr></hr>

        {node.settings && (
            <div className="space-y-3 mb-4">
            {node.settings.map(setting => (
                <SettingRow key={setting.domain + "." + setting.setting_name} depth={depth} setting={setting} values={values} errors={errors} updateValue={updateValue}/>
            ))}
            </div>
        )}

        {node.children &&
            Object.entries(node.children).map(([childName, childNode]) => (
            <DomainNode
                key={childName}
                name={toTitleCase(childName)}
                node={childNode}
                depth={depth + 1}
                values={values}
                errors={errors}
                updateValue={updateValue}
            />
            ))}
        </section>
    );
}

function SettingRow({ setting, depth, values, errors , updateValue}) {
    const value = values[setting.domain + "." + setting.setting_name];
    const error = errors[setting.domain + "." + setting.setting_name];

    return (
        <div style={{ marginLeft: (depth + 1) * 12 }}>
        <div className="flex justify-between items-center">
            <div>
            <div className="font-medium">{setting.setting_name}</div>
            <div className="text-sm text-gray-400">
                {setting.description}
            </div>
            </div>

            <SettingInput
            setting={setting}
            value={value}
            onChange={updateValue}
            />
        </div>

        {error && (
            <div className="text-sm text-red-400 mt-1">
            {error}
            </div>
        )}
        </div>
    );
}