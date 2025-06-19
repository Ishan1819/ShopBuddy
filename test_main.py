from backend.crew_config.crew_setup import create_crew

if __name__ == "__main__":
    print("🛒 Welcome to ShopBuddyAI!")
    user_query = input("Enter your shopping request: ")
    print(user_query)
    crew = create_crew(user_query)

    print("\n🤖 Crew is working on your query...")
    result = crew.kickoff()
    print("\n✅ Result:\n", result)
