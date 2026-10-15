
from decimal import Decimal
from Src.susu import SusuGroup

def format_money(amount):
    return f"GHS {amount:.2f}"


def show_report(group):
    report = group.get_report()

    print("\n========== SUSU GROUP REPORT ==========")
    print(f"Current week: {report['current_week']}")
    print(
        f"Weekly contribution: "
        f"{format_money(report['weekly_contribution'])}"
    )

    print("\nMember contributions:")
    for member, details in report["members"].items():
        paid = details["paid"]
        owes = details["owes"]

        if owes == Decimal("0.00"):
            status = "PAID IN FULL"
        elif paid == Decimal("0.00"):
            status = "NOT PAID"
        else:
            status = "PARTIALLY PAID"

        print(
            f"- {member}: Paid {format_money(paid)}, "
            f"Owes {format_money(owes)} [{status}]"
        )

    print("\nPayout history:")
    if not report["payout_history"]:
        print("No payouts yet.")
    else:
        for payout in report["payout_history"]:
            print(
                f"- Week {payout['week']}: "
                f"{payout['recipient']} received "
                f"{format_money(payout['amount'])}"
            )

    print("=======================================\n")


def main():
    print("Welcome to Susu Group Tracker!")

    while True:
        try:
            amount = input(
                "Enter the fixed weekly contribution in GHS: "
            ).strip()
            group = SusuGroup(amount)
            break
        except ValueError as error:
            print(f"Error: {error} Please try again.")

    print("\nGroup created successfully!")

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add member")
        print("2. Record contribution")
        print("3. Close current week")
        print("4. Show report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Enter member name: ").strip()
                group.add_member(name)
                print(f"{name} added successfully.")

            elif choice == "2":
                name = input("Enter member name: ").strip()
                amount = input(
                    "Enter payment amount in GHS: "
                ).strip()

                group.record_contribution(name, amount)
                print("Contribution recorded successfully.")

            elif choice == "3":
                result = group.close_week()

                if not result["closed"]:
                    print(
                        f"Week {result['week']} cannot close yet."
                    )
                    print("Outstanding contributions:")

                    for member, owed in result["owing"].items():
                        print(
                            f"- {member} owes "
                            f"{format_money(owed)}"
                        )
                else:
                    payout = result["payout"]
                    print(f"\nWeek {result['week']} closed!")
                    print(
                        f"{payout['recipient']} receives "
                        f"{format_money(payout['amount'])}"
                    )
                    print(
                        f"Week {group.current_week} has now begun."
                    )

            elif choice == "4":
                show_report(group)

            elif choice == "5":
                print("Thank you for using Susu Group Tracker!")
                break

            else:
                print("Invalid option. Choose a number from 1 to 5.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
