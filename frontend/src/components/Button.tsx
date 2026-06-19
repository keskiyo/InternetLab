import { cn } from '@/lib/cn'
import type { ButtonProps } from '@/types'
import { Spinner } from './Spinner'

const VARIANTS: Record<NonNullable<ButtonProps['variant']>, string> = {
	primary:
		'bg-accent text-white hover:bg-accent-hover shadow-sm focus-visible:ring-accent',
	ghost: 'bg-transparent text-fg-muted hover:text-fg hover:bg-surface-muted focus-visible:ring-accent',
}

export function Button({
	variant = 'primary',
	loading = false,
	disabled,
	className,
	children,
	...rest
}: ButtonProps): JSX.Element {
	return (
		<button
			className={cn(
				'inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-xl px-5 py-2.5',
				'text-sm font-medium transition-all duration-200 active:scale-[0.98]',
				'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
				'focus-visible:ring-offset-[rgb(var(--bg))]',
				'disabled:cursor-not-allowed disabled:opacity-50',
				VARIANTS[variant],
				className,
			)}
			disabled={disabled || loading}
			{...rest}
		>
			{loading && <Spinner />}
			{children}
		</button>
	)
}
