import { useCallback } from 'react'
import type { ParamDef } from '@/lib/types'

interface Props {
  param: ParamDef
  value: string
  onChange: (name: string, value: string) => void
}

export function ParamSelect({ param, value, onChange }: Props) {
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      onChange(param.name, e.target.value)
    },
    [param.name, onChange]
  )

  return (
    <div className="flex items-center gap-3 py-1.5">
      <label className="w-40 shrink-0 text-sm text-muted-foreground truncate" title={param.description}>
        {param.display_name}
      </label>
      <select
        value={value}
        onChange={handleChange}
        className="flex-1 px-3 py-1.5 text-sm bg-zinc-800 border border-border rounded-md
          focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
      >
        {param.choices?.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
    </div>
  )
}
