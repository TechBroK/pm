import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import LoginPage from "@/components/LoginPage";

vi.mock("@/lib/auth-context", () => ({
  useAuth: () => ({
    login: vi.fn(),
    signup: vi.fn(),
  }),
}));

describe("LoginPage", () => {
  it("prefills the default login credentials", () => {
    render(<LoginPage />);

    expect(screen.getByLabelText(/username/i)).toHaveValue("user");
    expect(screen.getByLabelText(/password/i)).toHaveValue("password");
  });
});