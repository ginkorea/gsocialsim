import { useCallback } from 'react'
import type { ParamDef } from '@/lib/types'
import { RotateCcw } from 'lucide-react'

interface Props {
  param: ParamDef
  value: number
  onChange: (name: string, value: number) => void
}

export function ParamSlider({ param, value, onChange }: Props) {
  const handleSlider = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange(param.name, parseFloat(e.target.value))
    },
    [param.name, onChange]
  )

  const handleInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const v = parseFloat(e.target.value)
      if (!isNaN(v)) onChange(param.name, v)
    },
    [param.name, onChange]
  )

  const handleReset = useCallback(() => {
    onChange(param.name, param.default as number)
  }, [param.name, param.default, onChange])

  const isModified = value !== param.default

  return (
    <div className="group flex items-center gap-3 py-1.5">
      <label className="w-40 shrink-0 text-sm text-muted-foreground truncate" title={param.description}>
        {param.display_name}
      </label>
      <input
        type="range"
        min={param.min ?? 0}
        max={param.max ?? 1}
        step={param.step ?? 0.01}
        value={value}
        onChange={handleSlider}
        className="flex-1 h-1.5 appearance-none bg-zinc-700 rounded-full cursor-pointer accent-primary
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:h-3.5
          [&::-webkit-slider-thumb]:bg-primary [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer
          [&::-webkit-slider-thumb]:shadow-[0_0_8px_rgba(59,130,246,0.4)]"
      />
      <input
        type="number"
        min={param.min}
        max={param.max}
        step={param.step}
        value={value}
        onChange={handleInput}
        className="w-20 px-2 py-1 text-xs text-right bg-zinc-800 border border-border rounded-md
          focus:outline-none focus:ring-1 focus:ring-primary"
      />
      <button
        onClick={handleReset}
        className={`p-1 rounded transition-opacity ${
          isModified ? 'opacity-100 text-muted-foreground hover:text-foreground' : 'opacity-0'
        }`}
        title="Reset to default"
      >
        <RotateCcw className="w-3.5 h-3.5" />
      </button>
    </div>
  )
}
