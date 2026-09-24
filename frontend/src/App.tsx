import type { ReactNode } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./auth";
import {
  Home,
  About,
  Courses,
  CourseDetails,
  Instructors,
  FAQ,
  Contact,
  Login,
  Register,
  ForgotPassword,
  ResetPassword,
  Verification,
  Dashboard,
  GenericPage,
} from "./pages";

function Protected({ children, role }: { children: ReactNode; role?: string }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (role && user.role !== role) return <Navigate to={`/${user.role}/dashboard`} replace />;
  return children;
}

const roleKeys = {
  student: [
    "dashboard", "my-courses", "course-player", "lessons", "assignments", "quizzes", "exams",
    "calendar", "progress", "certificates", "messages", "notifications", "profile", "settings",
  ],
  instructor: [
    "dashboard", "courses", "create-course", "lessons", "assignments", "quizzes", "exams", "students",
    "gradebook", "attendance", "live-classes", "messages", "profile", "settings",
  ],
  admin: [
    "dashboard", "users", "instructors", "courses", "categories", "enrollments", "assignments", "quizzes",
    "exams", "certificates", "reviews", "reports", "notifications", "support", "profile", "settings",
  ],
} as const;

function RoleRoutes({ role }: { role: keyof typeof roleKeys }) {
  return (
    <Routes>
      {roleKeys[role].map((key) => (
        <Route
          key={key}
          path={key}
          element={
            <Protected role={role}>
              {key === "dashboard" ? <Dashboard role={role} /> : <GenericPage role={role} keyName={key} />}
            </Protected>
          }
        />
      ))}
      <Route path="*" element={<Navigate to="dashboard" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/courses/:slug" element={<CourseDetails />} />
        <Route path="/instructors" element={<Instructors />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/verification" element={<Verification />} />
        <Route path="/student/*" element={<RoleRoutes role="student" />} />
        <Route path="/instructor/*" element={<RoleRoutes role="instructor" />} />
        <Route path="/admin/*" element={<RoleRoutes role="admin" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}
