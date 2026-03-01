import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <header className="absolute inset-x-0 top-0 z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1">
            <a href="#" className="-m-1.5 p-1.5 overflow-hidden">
              <span className="sr-only">Stride</span>
              <h1 className="text-2xl font-black text-blue-600">Stride</h1>
            </a>
          </div>
          <div className="flex flex-1 justify-end gap-x-4">
            <Link href="/login" className="text-sm font-semibold leading-6 text-gray-900 px-3 py-2 rounded-md hover:bg-gray-50">
              Log in
            </Link>
            <Link href="/register" className="text-sm font-semibold leading-6 text-white bg-blue-600 px-4 py-2 rounded-md hover:bg-blue-700">
              Sign up <span aria-hidden="true">&rarr;</span>
            </Link>
          </div>
        </nav>
      </header>

      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-balance text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Turn your to-do list into a social experience
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Stride is a productivity-focused platform that empowers you to share and complete tasks, fostering a supportive and motivating community.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/register"
                className="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              >
                Get started
              </Link>
              <Link href="/login" className="text-sm font-semibold leading-6 text-gray-900 px-3.5 py-2.5 rounded hover:bg-gray-50">
                Log in
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
