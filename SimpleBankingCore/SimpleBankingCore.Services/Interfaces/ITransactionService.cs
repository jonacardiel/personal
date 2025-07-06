using SimpleBankingCore.Core.Models;
using System.Threading.Tasks;

namespace SimpleBankingCore.Services.Interfaces
{
    public interface ITransactionService
    {
        Task<Account> DepositAsync(int accountId, decimal amount, string description = "Deposit");
        Task<Account> WithdrawAsync(int accountId, decimal amount, string description = "Withdrawal");
        Task TransferAsync(int fromAccountId, int toAccountId, decimal amount, string description = "Transfer");
    }
}
