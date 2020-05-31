import React from "react"
import { BrowserRouter as Router } from "react-router-dom"
import {
  AuthContext,
  AuthModalProvider,
  CategoriesContext,
  ForumStatsContext,
  SettingsContext,
  ToastsContextProvider,
} from "../Context"
import Routes from "../Routes"
import { RouteErrorBoundary } from "../UI"
import AppDataQuery from "./AppDataQuery"
import AppErrorBoundary from "./AppErrorBoundary"
import AppLanguageLoader from "./AppLanguageLoader"

const Navbar = React.lazy(() => import("../Navbar"))
const Toasts = React.lazy(() => import("../Toasts"))
const AuthChangedAlert = React.lazy(() => import("../AuthChangedAlert"))
const AuthModal = React.lazy(() => import("../AuthModal"))

const App: React.FC = () => {
  return (
    <AppErrorBoundary>
      <Router>
        <AppDataQuery>
          {({ data: { auth, categories, forumStats, settings } }) => (
            <AppLanguageLoader language="en">
              <AuthContext.Provider value={auth}>
                <CategoriesContext.Provider value={categories}>
                  <SettingsContext.Provider value={settings}>
                    <ToastsContextProvider>
                      <ForumStatsContext.Provider value={forumStats}>
                        <AuthModalProvider>
                          <React.Suspense fallback={<div />}>
                            <AuthChangedAlert user={auth} />
                          </React.Suspense>
                          <React.Suspense fallback={<div />}>
                            <Navbar settings={settings} user={auth} />
                            <Toasts />
                          </React.Suspense>
                          <RouteErrorBoundary>
                            <Routes />
                          </RouteErrorBoundary>
                          <React.Suspense fallback={<div />}>
                            <AuthModal settings={settings} />
                          </React.Suspense>
                        </AuthModalProvider>
                      </ForumStatsContext.Provider>
                    </ToastsContextProvider>
                  </SettingsContext.Provider>
                </CategoriesContext.Provider>
              </AuthContext.Provider>
            </AppLanguageLoader>
          )}
        </AppDataQuery>
      </Router>
    </AppErrorBoundary>
  )
}

export default App
