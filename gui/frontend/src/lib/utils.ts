import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M'
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K'
  return n.toString()
}

export function leanToColor(lean: number): string {
  // -1 = blue, 0 = gray, 1 = red
  if (lean < 0) {
    const intensity = Math.min(Math.abs(lean), 1)
    const r = Math.round(59 * (1 - intensity))
    const g = Math.round(130 * (1 - intensity * 0.3))
    const b = Math.round(246)
    return `rgb(${r},${g},${b})`
  } else {
    const intensity = Math.min(lean, 1)
    const r = Math.round(239)
    const g = Math.round(68 * (1 - intensity * 0.5))
    const b = Math.round(68 * (1 - intensity * 0.5))
    return `rgb(${r},${g},${b})`
  }
}

export function polarizationLabel(variance: number): string {
  if (variance < 0.1) return 'Low'
  if (variance < 0.3) return 'Moderate'
  if (variance < 0.5) return 'High'
  return 'Extreme'
}
