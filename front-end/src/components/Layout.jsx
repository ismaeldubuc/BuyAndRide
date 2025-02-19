import Header from './Header';

function Layout({ children }) {
    return (
        <div>
            <Header />
            <main className="p-4">
                {children}
            </main>
        </div>
    );
}

export default Layout;
