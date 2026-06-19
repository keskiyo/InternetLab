import { ThemeToggle } from '@/components/ThemeToggle'
import { ContactForm } from '@/features/ContactForm'
import { HeroSection } from '@/features/HeroSection'

export default function App(): JSX.Element {
	return (
		<div className='bg-app min-h-dvh'>
			<header className='border-app border-b'>
				<div className='mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8'>
					<div className='flex items-center gap-2'>
						<span className='font-heading font-semibold text-fg'>
							Backend
						</span>
					</div>
					<ThemeToggle />
				</div>
			</header>

			<main className='mx-auto max-w-6xl space-y-20 px-5 py-16 sm:px-8 sm:py-24'>
				<HeroSection />
				<ContactForm />
			</main>

			<footer className='border-app border-t'>
				<div className='text-fg-muted mx-auto max-w-6xl px-5 py-6 text-center text-xs sm:px-8'>
					FastAPI + React + YandexGPT
				</div>
			</footer>
		</div>
	)
}
