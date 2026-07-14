import { z } from "zod";

const passwordSchema = z
  .string()
  .min(12, "Password must contain at least 12 characters.")
  .max(128, "Password must contain no more than 128 characters.")
  .regex(/[A-Z]/, "Password must include an uppercase letter.")
  .regex(/[a-z]/, "Password must include a lowercase letter.")
  .regex(/[0-9]/, "Password must include a number.")
  .regex(/[^A-Za-z0-9]/, "Password must include a special character.");

export const registerSchema = z
  .object({
    username: z
      .string()
      .min(3, "Username must contain at least 3 characters.")
      .max(50, "Username must contain no more than 50 characters.")
      .regex(
        /^[A-Za-z0-9_-]+$/,
        "Username may contain letters, numbers, underscores, and hyphens.",
      ),
    email: z
      .email("Enter a valid email address.")
      .max(254, "Email address is too long."),
    password: passwordSchema,
    confirmPassword: z.string(),
  })
  .refine((values) => values.password === values.confirmPassword, {
    message: "Passwords do not match.",
    path: ["confirmPassword"],
  });

export type RegisterFormValues = z.infer<typeof registerSchema>;