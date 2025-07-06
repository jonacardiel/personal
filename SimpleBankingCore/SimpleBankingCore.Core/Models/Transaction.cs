using SimpleBankingCore.Core.Enums;
using System;

namespace SimpleBankingCore.Core.Models
{
    // Represents an immutable financial transaction (the core of your custom ledger)
    public class Transaction
    {
        public int TransactionId { get; set; } // Primary Key
        public int AccountId { get; set; } // Foreign Key to Account
        public TransactionType TransactionType { get; set; }
        public decimal Amount { get; set; }
        public DateTime TransactionDate { get; set; } = DateTime.UtcNow;
        public string Description { get; set; } = string.Empty;
        public decimal BalanceAfterTransaction { get; set; }

        // Navigation property
        public Account? Account { get; set; }
    }
}
