export default function Table({data, columns}) {
    return (
    <div className="overflow-x-auto rounded-2xl border border-(--color-text)/9">
      <table className="w-full text-sm text-left">
        <thead className="text-(--color-text) border-b border-(--color-text)/9 bg-(--color-header)">
          <tr>
            {columns.map(col => (
              <th key={col.key} className="px-3 py-4">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map(row => (
            <tr
              key={row.id}
              className="border-b border-gray-800 hover:bg-(--color-background-accent)"
            >
              {columns.map(col => (
                <td key={col.key} className="px-3 py-2 border-b border-(--color-text)/9">
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