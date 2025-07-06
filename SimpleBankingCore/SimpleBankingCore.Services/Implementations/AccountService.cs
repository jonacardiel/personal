using System;
using SimpleBankingCore.Core.Models;
using SimpleBankingCore.Core.Enums;
using SimpleBankingCore.Data.Repositories;
using SimpleBankingCore.Services.Interfaces;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using System.Linq;

#nullable enable

namespace SimpleBankingCore.Services.Implementations
{
    public class AccountService : IAccountService
    {
        private readonly IRepository<Account> _accountRepository;
        private readonly IRepository<Customer> _customerRepository;
        private readonly IRepository<Transaction> _transactionRepository;

        public AccountService(IRepository<Account> accountRepository, IRepository<Customer> customerRepository, IRepository<Transaction> transactionRepository)
        {
            _accountRepository = accountRepository;
            _customerRepository = customerRepository;
            _transactionRepository = transactionRepository;
        }

        public async Task<Account> CreateAccountAsync(int customerId, AccountType accountType, decimal initialBalance = 0.00m)
        {
            var customer = await _customerRepository.GetByIdAsync(customerId);
            if (customer == null)
            {
                throw new ArgumentException($"Customer with ID {customerId} not found.");
            }
            if (initialBalance < 0)
            {
                throw new ArgumentException("Initial balance cannot be negative.");
            }

            var account = new Account
            {
                CustomerId = customerId,
                AccountType = accountType,
                CurrentBalance = initialBalance,
                IsActive = true
            };

            await _accountRepository.AddAsync(account);
            await _accountRepository.SaveChangesAsync();

            if (initialBalance > 0)
            {
                var initialDeposit = new Transaction
                {
                    AccountId = account.AccountId,
                    TransactionType = TransactionType.Deposit,
                    Amount = initialBalance,
                    Description = "Initial Deposit",
                    BalanceAfterTransaction = initialBalance
                };
                await _transactionRepository.AddAsync(initialDeposit);
                await _transactionRepository.SaveChangesAsync();
            }

            return account;
        }

        public async Task<Account?> GetAccountByIdAsync(int accountId)
        {
            // Use repository method to include Transactions
            return await _accountRepository.GetSingleOrDefaultAsync(
                a => a.AccountId == accountId,
                a => a.Transactions
            );
        }

        public async Task<IEnumerable<Account>> GetAccountsByCustomerIdAsync(int customerId)
        {
            // Use repository method to filter by CustomerId
            return await _accountRepository.FindAsync(a => a.CustomerId == customerId);
        }

        public async Task<IEnumerable<Transaction>> GetAccountTransactionsAsync(int accountId)
        {
            // Use transaction repository to filter by AccountId and order by TransactionDate
            var transactions = await _transactionRepository.FindAsync(t => t.AccountId == accountId);
            return transactions.OrderBy(t => t.TransactionDate);
        }

        public async Task CloseAccountAsync(int accountId)
        {
            var account = await _accountRepository.GetByIdAsync(accountId);
            if (account == null)
            {
                throw new ArgumentException($"Account with ID {accountId} not found.");
            }
            if (account.CurrentBalance != 0)
            {
                throw new InvalidOperationException($"Cannot close account {accountId} with a non-zero balance. Current balance: {account.CurrentBalance:C}");
            }

            account.IsActive = false;
            await _accountRepository.UpdateAsync(account);
            await _accountRepository.SaveChangesAsync();
        }
    }
}
