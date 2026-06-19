import { Moon, Sun } from 'lucide-react'

import { useTheme } from '@/hooks/useTheme'

export function ThemeToggle(): JSX.Element {
	const { theme, toggleTheme } = useTheme()
	const isDark = theme === 'dark'
	return (
		<button
			type='button'
			onClick={toggleTheme}
			aria-label={
				isDark ? 'Включить светлую тему' : 'Включить тёмную тему'
			}
			className='border-app bg-surface text-fg-muted hover:text-fg flex h-11 w-11 cursor-pointer items-center justify-center rounded-xl border transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent'
		>
			{isDark ? (
				<Sun className='h-5 w-5' />
			) : (
				<Moon className='h-5 w-5' />
			)}
		</button>
	)
}
