#nullable enable
using SimpleBankingCore.Core.Models;
using SimpleBankingCore.Core.Enums;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace SimpleBankingCore.Services.Interfaces
{
    public interface IAccountService
    {
        Task<Account> CreateAccountAsync(int customerId, AccountType accountType, decimal initialBalance = 0.00m);
        Task<Account?> GetAccountByIdAsync(int accountId);
        Task<IEnumerable<Account>> GetAccountsByCustomerIdAsync(int customerId);
        Task<IEnumerable<Transaction>> GetAccountTransactionsAsync(int accountId);
        Task CloseAccountAsync(int accountId);
    }
}
