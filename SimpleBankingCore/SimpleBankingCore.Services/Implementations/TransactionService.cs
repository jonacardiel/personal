using System;
using SimpleBankingCore.Core.Models;
using SimpleBankingCore.Core.Enums;
using SimpleBankingCore.Core.Exceptions;
using SimpleBankingCore.Data.Repositories;
using SimpleBankingCore.Services.Interfaces;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace SimpleBankingCore.Services.Implementations
{
    public class TransactionService : ITransactionService
    {
        private readonly IRepository<Account> _accountRepository;
        private readonly IRepository<Transaction> _transactionRepository;

        public TransactionService(IRepository<Account> accountRepository, IRepository<Transaction> transactionRepository)
        {
            _accountRepository = accountRepository;
            _transactionRepository = transactionRepository;
        }

        public async Task<Account> DepositAsync(int accountId, decimal amount, string description = "Deposit")
        {
            if (amount <= 0)
            {
                throw new ArgumentException("Deposit amount must be positive.");
            }

            var account = await _accountRepository.GetByIdAsync(accountId);

            if (account == null || !account.IsActive)
            {
                throw new ArgumentException($"Account with ID {accountId} not found or is inactive.");
            }

            account.CurrentBalance += amount;

            var transaction = new Transaction
            {
                AccountId = accountId,
                TransactionType = TransactionType.Deposit,
                Amount = amount,
                Description = description,
                BalanceAfterTransaction = account.CurrentBalance
            };

            await _transactionRepository.AddAsync(transaction);
            await _accountRepository.UpdateAsync(account);

            await _accountRepository.SaveChangesAsync();

            return account;
        }

        public async Task<Account> WithdrawAsync(int accountId, decimal amount, string description = "Withdrawal")
        {
            if (amount <= 0)
            {
                throw new ArgumentException("Withdrawal amount must be positive.");
            }

            var account = await _accountRepository.GetByIdAsync(accountId);

            if (account == null || !account.IsActive)
            {
                throw new ArgumentException($"Account with ID {accountId} not found or is inactive.");
            }

            if (account.CurrentBalance < amount)
            {
                throw new InsufficientFundsException($"Account {accountId} has insufficient funds. Current: {account.CurrentBalance:C}, Attempted withdrawal: {amount:C}");
            }

            account.CurrentBalance -= amount;

            var transaction = new Transaction
            {
                AccountId = accountId,
                TransactionType = TransactionType.Withdrawal,
                Amount = amount,
                Description = description,
                BalanceAfterTransaction = account.CurrentBalance
            };

            await _transactionRepository.AddAsync(transaction);
            await _accountRepository.UpdateAsync(account);

            await _accountRepository.SaveChangesAsync();

            return account;
        }

        public async Task TransferAsync(int fromAccountId, int toAccountId, decimal amount, string description = "Transfer")
        {
            if (amount <= 0)
            {
                throw new ArgumentException("Transfer amount must be positive.");
            }
            if (fromAccountId == toAccountId)
            {
                throw new ArgumentException("Cannot transfer to the same account.");
            }

            var fromAccount = await _accountRepository.GetByIdAsync(fromAccountId);
            var toAccount = await _accountRepository.GetByIdAsync(toAccountId);

            if (fromAccount == null || !fromAccount.IsActive)
            {
                throw new ArgumentException($"Source account with ID {fromAccountId} not found or is inactive.");
            }
            if (toAccount == null || !toAccount.IsActive)
            {
                throw new ArgumentException($"Destination account with ID {toAccountId} not found or is inactive.");
            }

            if (fromAccount.CurrentBalance < amount)
            {
                throw new InsufficientFundsException($"Source account {fromAccountId} has insufficient funds. Current: {fromAccount.CurrentBalance:C}, Attempted transfer: {amount:C}");
            }

            fromAccount.CurrentBalance -= amount;
            toAccount.CurrentBalance += amount;

            var transferOutTransaction = new Transaction
            {
                AccountId = fromAccountId,
                TransactionType = TransactionType.TransferOut,
                Amount = amount,
                Description = $"Transfer to Account {toAccountId}: {description}",
                BalanceAfterTransaction = fromAccount.CurrentBalance
            };

            var transferInTransaction = new Transaction
            {
                AccountId = toAccountId,
                TransactionType = TransactionType.TransferIn,
                Amount = amount,
                Description = $"Transfer from Account {fromAccountId}: {description}",
                BalanceAfterTransaction = toAccount.CurrentBalance
            };

            await _transactionRepository.AddAsync(transferOutTransaction);
            await _transactionRepository.AddAsync(transferInTransaction);
            await _accountRepository.UpdateAsync(fromAccount);
            await _accountRepository.UpdateAsync(toAccount);

            await _accountRepository.SaveChangesAsync();
        }
    }
}
