using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using SimpleBankingCore.Core.Enums;
using SimpleBankingCore.Core.Exceptions;
using SimpleBankingCore.Core.Models;
using SimpleBankingCore.Data.Context;
using SimpleBankingCore.Data.Repositories;
using SimpleBankingCore.Services.Implementations;
using SimpleBankingCore.Services.Interfaces;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace SimpleBankingCore.App
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();

            using (var scope = host.Services.CreateScope())
            {
                var dbContext = scope.ServiceProvider.GetRequiredService<BankingDbContext>();
                try
                {
                    Console.WriteLine("Applying database migrations...");
                    await dbContext.Database.MigrateAsync();
                    Console.WriteLine("Database migrations applied successfully.");
                }
                catch (Exception ex)
                {
                    var migrationLogger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
                    migrationLogger.LogError(ex, "An error occurred while applying database migrations.");
                }
            }

            var customerService = host.Services.GetRequiredService<ICustomerService>();
            var accountService = host.Services.GetRequiredService<IAccountService>();
            var transactionService = host.Services.GetRequiredService<ITransactionService>();
            var logger = host.Services.GetRequiredService<ILogger<Program>>();

            await RunApplication(customerService, accountService, transactionService, logger);
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureAppConfiguration((hostingContext, config) =>
                {
                    config.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);
                    config.AddEnvironmentVariables();
                })
                .ConfigureServices((hostContext, services) =>
                {
                    
                    services.AddDbContext<BankingDbContext>(options =>
                        options.UseSqlite(hostContext.Configuration.GetConnectionString("DefaultConnection")));

                    services.AddScoped(typeof(IRepository<>), typeof(GenericRepository<>));
                    services.AddScoped<ICustomerService, CustomerService>();
                    services.AddScoped<IAccountService, AccountService>();
                    services.AddScoped<ITransactionService, TransactionService>();
                    services.AddScoped<CustomerRepository>();

                    services.AddLogging(configure => configure.AddConsole());
                });

        public static async Task RunApplication(
            ICustomerService customerService,
            IAccountService accountService,
            ITransactionService transactionService,
            ILogger<Program> logger)
        {
            Console.WriteLine("\n--- Simple Banking Core Application ---");

            while (true)
            {
                Console.WriteLine("\nMenu:");
                Console.WriteLine("1. Create Customer");
                Console.WriteLine("2. List All Customers");
                Console.WriteLine("3. Create Account for Customer");
                Console.WriteLine("4. View Customer Accounts & Balances");
                Console.WriteLine("5. View Account Transactions");
                Console.WriteLine("6. Deposit Funds");
                Console.WriteLine("7. Withdraw Funds");
                Console.WriteLine("8. Transfer Funds");
                Console.WriteLine("9. Close Account");
                Console.WriteLine("0. Exit");
                Console.Write("Enter your choice: ");

                var choice = Console.ReadLine();
                Console.WriteLine();

                try
                {
                    switch (choice)
                    {
                        case "1":
                            await CreateCustomer(customerService, logger);
                            break;
                        case "2":
                            await ListAllCustomers(customerService, logger);
                            break;
                        case "3":
                            await CreateAccountForCustomer(customerService, accountService, logger);
                            break;
                        case "4":
                            await ViewCustomerAccounts(customerService, accountService, logger);
                            break;
                        case "5":
                            await ViewAccountTransactions(accountService, logger);
                            break;
                        case "6":
                            await DepositFunds(transactionService, accountService, logger);
                            break;
                        case "7":
                            await WithdrawFunds(transactionService, accountService, logger);
                            break;
                        case "8":
                            await TransferFunds(transactionService, accountService, logger);
                            break;
                        case "9":
                            await CloseAccount(accountService, logger);
                            break;
                        case "0":
                            Console.WriteLine("Exiting application. Goodbye!");
                            return;
                        default:
                            Console.WriteLine("Invalid choice. Please try again.");
                            break;
                    }
                }
                catch (Exception ex)
                {
                    if (ex is ArgumentException || ex is InvalidOperationException || ex is InsufficientFundsException)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine($"Error: {ex.Message}");
                        Console.ResetColor();
                    }
                    else
                    {
                        logger.LogError(ex, "An unexpected error occurred: {Message}", ex.Message);
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("An unexpected error occurred. Please check the logs.");
                        Console.ResetColor();
                    }
                }
                Console.WriteLine("\nPress any key to continue...");
                Console.ReadKey();
            }
        }

        #region Menu Handlers

        private static async Task CreateCustomer(ICustomerService customerService, ILogger<Program> logger)
        {
            Console.Write("Enter customer first name: ");
            var firstName = Console.ReadLine() ?? string.Empty;
            Console.Write("Enter customer last name: ");
            var lastName = Console.ReadLine() ?? string.Empty;
            Console.Write("Enter customer email: ");
            var email = Console.ReadLine() ?? string.Empty;

            if (string.IsNullOrWhiteSpace(firstName) || string.IsNullOrWhiteSpace(lastName) || string.IsNullOrWhiteSpace(email))
            {
                Console.WriteLine("All fields are required.");
                return;
            }

            try
            {
                var customer = await customerService.CreateCustomerAsync(firstName, lastName, email);
                Console.WriteLine($"Customer created successfully! ID: {customer.CustomerId}, Name: {customer.FirstName} {customer.LastName}");
            }
            catch (InvalidOperationException ex)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"Warning: {ex.Message}");
                Console.ResetColor();
            }
        }

        private static async Task ListAllCustomers(ICustomerService customerService, ILogger<Program> logger)
        {
            var customers = await customerService.GetAllCustomersAsync();
            if (!customers.Any())
            {
                Console.WriteLine("No customers found.");
                return;
            }

            Console.WriteLine("--- All Customers ---");
            foreach (var customer in customers)
            {
                Console.WriteLine($"ID: {customer.CustomerId}, Name: {customer.FirstName} {customer.LastName}, Email: {customer.Email}, Created: {customer.DateCreated:yyyy-MM-dd}");
            }
        }

        private static async Task CreateAccountForCustomer(ICustomerService customerService, IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Customer ID to create account for: ");
            if (!int.TryParse(Console.ReadLine(), out int customerId))
            {
                Console.WriteLine("Invalid Customer ID.");
                return;
            }

            var customer = await customerService.GetCustomerByIdAsync(customerId);
            if (customer == null)
            {
                Console.WriteLine($"Customer with ID {customerId} not found.");
                return;
            }

            Console.Write("Enter Account Type (Checking/Savings): ");
            var accountTypeInput = Console.ReadLine();
            if (!Enum.TryParse(accountTypeInput, true, out AccountType accountType))
            {
                Console.WriteLine("Invalid Account Type. Please enter 'Checking' or 'Savings'.");
                return;
            }

            Console.Write("Enter Initial Balance (optional, default 0): ");
            decimal initialBalance = 0.00m;
            var balanceInput = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(balanceInput) && !decimal.TryParse(balanceInput, out initialBalance))
            {
                Console.WriteLine("Invalid balance amount. Setting to 0.");
            }

            try
            {
                var account = await accountService.CreateAccountAsync(customerId, accountType, initialBalance);
                Console.WriteLine($"Account created successfully! Account ID: {account.AccountId}, Type: {account.AccountType}, Balance: {account.CurrentBalance:C}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static async Task ViewCustomerAccounts(ICustomerService customerService, IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Customer ID to view accounts for: ");
            if (!int.TryParse(Console.ReadLine(), out int customerId))
            {
                Console.WriteLine("Invalid Customer ID.");
                return;
            }

            var customer = await customerService.GetCustomerByIdAsync(customerId);
            if (customer == null)
            {
                Console.WriteLine($"Customer with ID {customerId} not found.");
                return;
            }

            Console.WriteLine($"--- Accounts for {customer.FirstName} {customer.LastName} (ID: {customer.CustomerId}) ---");
            if (customer.Accounts.Any())
            {
                foreach (var account in customer.Accounts)
                {
                    Console.WriteLine($"  Account ID: {account.AccountId}, Type: {account.AccountType}, Balance: {account.CurrentBalance:C}, Active: {account.IsActive}");
                }
            }
            else
            {
                Console.WriteLine("  No accounts found for this customer.");
            }
        }

        private static async Task ViewAccountTransactions(IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Account ID to view transactions for: ");
            if (!int.TryParse(Console.ReadLine(), out int accountId))
            {
                Console.WriteLine("Invalid Account ID.");
                return;
            }

            var account = await accountService.GetAccountByIdAsync(accountId);
            if (account == null)
            {
                Console.WriteLine($"Account with ID {accountId} not found.");
                return;
            }

            Console.WriteLine($"--- Transactions for Account {account.AccountId} ({account.AccountType}, Current Balance: {account.CurrentBalance:C}) ---");
            var transactions = await accountService.GetAccountTransactionsAsync(accountId);

            if (!transactions.Any())
            {
                Console.WriteLine("No transactions found for this account.");
                return;
            }

            Console.WriteLine("ID\tType\t\tAmount\t\tBalance After\tDate\t\tDescription");
            Console.WriteLine("--\t----\t\t------\t\t-------------\t----\t\t-----------");
            foreach (var transaction in transactions)
            {
                Console.WriteLine($"{transaction.TransactionId}\t{transaction.TransactionType}\t{transaction.Amount:C}\t\t{transaction.BalanceAfterTransaction:C}\t\t{transaction.TransactionDate:yyyy-MM-dd}\t\t{transaction.Description}");
            }
        }

        private static async Task DepositFunds(ITransactionService transactionService, IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Account ID to deposit into: ");
            if (!int.TryParse(Console.ReadLine(), out int accountId))
            {
                Console.WriteLine("Invalid Account ID.");
                return;
            }

            Console.Write("Enter amount to deposit: ");
            if (!decimal.TryParse(Console.ReadLine(), out decimal amount) || amount <= 0)
            {
                Console.WriteLine("Invalid amount. Please enter a positive number.");
                return;
            }

            Console.Write("Enter deposit description (optional): ");
            var description = Console.ReadLine() ?? "Deposit";

            try
            {
                var updatedAccount = await transactionService.DepositAsync(accountId, amount, description);
                Console.WriteLine($"Successfully deposited {amount:C} into Account {accountId}. New balance: {updatedAccount.CurrentBalance:C}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static async Task WithdrawFunds(ITransactionService transactionService, IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Account ID to withdraw from: ");
            if (!int.TryParse(Console.ReadLine(), out int accountId))
            {
                Console.WriteLine("Invalid Account ID.");
                return;
            }

            Console.Write("Enter amount to withdraw: ");
            if (!decimal.TryParse(Console.ReadLine(), out decimal amount) || amount <= 0)
            {
                Console.WriteLine("Invalid amount. Please enter a positive number.");
                return;
            }

            Console.Write("Enter withdrawal description (optional): ");
            var description = Console.ReadLine() ?? "Withdrawal";

            try
            {
                var updatedAccount = await transactionService.WithdrawAsync(accountId, amount, description);
                Console.WriteLine($"Successfully withdrew {amount:C} from Account {accountId}. New balance: {updatedAccount.CurrentBalance:C}");
            }
            catch (InsufficientFundsException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static async Task TransferFunds(ITransactionService transactionService, IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Source Account ID: ");
            if (!int.TryParse(Console.ReadLine(), out int fromAccountId))
            {
                Console.WriteLine("Invalid Source Account ID.");
                return;
            }

            Console.Write("Enter Destination Account ID: ");
            if (!int.TryParse(Console.ReadLine(), out int toAccountId))
            {
                Console.WriteLine("Invalid Destination Account ID.");
                return;
            }

            Console.Write("Enter amount to transfer: ");
            if (!decimal.TryParse(Console.ReadLine(), out decimal amount) || amount <= 0)
            {
                Console.WriteLine("Invalid amount. Please enter a positive number.");
                return;
            }

            Console.Write("Enter transfer description (optional): ");
            var description = Console.ReadLine() ?? "Bank Transfer";

            try
            {
                await transactionService.TransferAsync(fromAccountId, toAccountId, amount, description);
                var fromAccount = await accountService.GetAccountByIdAsync(fromAccountId);
                var toAccount = await accountService.GetAccountByIdAsync(toAccountId);
                Console.WriteLine($"Successfully transferred {amount:C} from Account {fromAccountId} (New Balance: {fromAccount?.CurrentBalance:C}) to Account {toAccountId} (New Balance: {toAccount?.CurrentBalance:C}).");
            }
            catch (InsufficientFundsException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static async Task CloseAccount(IAccountService accountService, ILogger<Program> logger)
        {
            Console.Write("Enter Account ID to close: ");
            if (!int.TryParse(Console.ReadLine(), out int accountId))
            {
                Console.WriteLine("Invalid Account ID.");
                return;
            }

            try
            {
                var account = await accountService.GetAccountByIdAsync(accountId);
                if (account == null)
                {
                    Console.WriteLine($"Account with ID {accountId} not found.");
                    return;
                }

                if (account.CurrentBalance != 0)
                {
                    Console.WriteLine($"Warning: Account {accountId} has a non-zero balance of {account.CurrentBalance:C}. Please withdraw/transfer funds before closing.");
                    return;
                }

                await accountService.CloseAccountAsync(accountId);
                Console.WriteLine($"Account {accountId} has been successfully closed.");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        #endregion
    }
}
