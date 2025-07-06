using System;
using System.Collections.Generic;

namespace SimpleBankingCore.Core.Models
{
    // Represents a bank customer
    public class Customer
    {
        public int CustomerId { get; set; } // Primary Key
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty; // Unique identifier for login/customer search
        public DateTime DateCreated { get; set; } = DateTime.UtcNow;

        // Navigation property: A customer can have many accounts
        public ICollection<Account> Accounts { get; set; } = new List<Account>();
    }
}
