import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
import type { ParamDef } from '@/lib/types'
import { ParamSlider } from './ParamSlider'
import { ParamSelect } from './ParamSelect'

interface Props {
  name: string
  params: ParamDef[]
  values: Record<string, number | string | boolean>
  onChange: (name: string, value: number | string | boolean) => void
}

export function ParamGroup({ name, params, values, onChange }: Props) {
  const [open, setOpen] = useState(true)

  return (
    <div className="glass rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-zinc-700/30 transition-colors"
      >
        <span className="text-sm font-medium">{name}</span>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{params.length} params</span>
          {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </div>
      </button>
      {open && (
        <div className="px-4 pb-3 space-y-0.5">
          {params.map((p) =>
            p.choices ? (
              <ParamSelect
                key={p.name}
                param={p}
                value={String(values[p.name] ?? p.default)}
                onChange={onChange}
              />
            ) : (
              <ParamSlider
                key={p.name}
                param={p}
                value={Number(values[p.name] ?? p.default)}
                onChange={onChange}
              />
            )
          )}
        </div>
      )}
    </div>
  )
}
