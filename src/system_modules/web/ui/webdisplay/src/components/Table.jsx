export default function Table({data, columns}) {
    return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-gray-400 border-b border-gray-700">
          <tr>
            {columns.map(col => (
              <th key={col.key} className="px-3 py-2">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map(row => (
            <tr
              key={row.id}
              className="border-b border-gray-800 hover:bg-gray-900/50"
            >
              {columns.map(col => (
                <td key={col.key} className="px-3 py-2 border-b border-gray-700">
                  {col.render
                    ? col.render(row[col.key], row)
                    : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}