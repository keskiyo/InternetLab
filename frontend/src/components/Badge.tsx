import { cn } from '@/lib/cn'
import type { BadgeProps, BadgeTone } from '@/types'

const TONES: Record<BadgeTone, string> = {
	positive:
		'bg-emerald-500/12 text-emerald-600 dark:text-emerald-400 ring-emerald-500/30',
	negative: 'bg-red-500/12 text-red-600 dark:text-red-400 ring-red-500/30',
	neutral:
		'bg-slate-500/12 text-slate-600 dark:text-slate-300 ring-slate-500/30',
	accent: 'bg-accent-soft text-accent ring-accent/30',
}

export function Badge({
	tone = 'neutral',
	icon,
	children,
}: BadgeProps): JSX.Element {
	return (
		<span
			className={cn(
				'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium ring-1 ring-inset',
				TONES[tone],
			)}
		>
			{icon}
			{children}
		</span>
	)
}
