from outreach.dm_generator import generate_dm

dm = generate_dm(
    company="ExampleAI",
    role="Software Engineer Intern",
    founder_name="Rahul",
    your_name="Niranjan"
)

print("=== GENERATED DM ===")
print(dm)
