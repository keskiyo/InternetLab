import { cn } from '@/lib/cn'
import type { CardProps } from '@/types'

export function Card({ className, children, ...rest }: CardProps): JSX.Element {
	return (
		<div
			className={cn(
				'bg-surface border-app rounded-xl border p-6 shadow-card sm:p-8',
				className,
			)}
			{...rest}
		>
			{children}
		</div>
	)
}
