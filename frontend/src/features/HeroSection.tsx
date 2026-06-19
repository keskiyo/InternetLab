import { ArrowDown } from 'lucide-react'

import { Button } from '@/components/Button'

const STACK = ['Python', 'FastAPI', 'SQLAlchemy', 'AI / LLM']

export function HeroSection(): JSX.Element {
	return (
		<section className='flex flex-col items-start gap-6 pt-4'>
			<div className='space-y-3'>
				<h1 className='font-heading text-4xl font-bold tracking-tight text-fg sm:text-5xl lg:text-6xl'>
					Привет, я Макс.
				</h1>
				<p className='text-fg-muted max-w-xl text-base leading-relaxed sm:text-lg'>
					Проект на Python и FastAPI — AI-интеграция.
				</p>
			</div>

			<ul className='flex flex-wrap gap-2'>
				{STACK.map(item => (
					<li
						key={item}
						className='bg-surface-muted text-fg-muted rounded-lg px-3 py-1 text-xs font-medium'
					>
						{item}
					</li>
				))}
			</ul>

			<div className='flex flex-wrap items-center gap-3 pt-2'>
				<Button
					onClick={() => {
						document
							.getElementById('contact')
							?.scrollIntoView({ behavior: 'smooth' })
					}}
				>
					Создать заявку
					<ArrowDown className='h-4 w-4' />
				</Button>
			</div>
		</section>
	)
}
